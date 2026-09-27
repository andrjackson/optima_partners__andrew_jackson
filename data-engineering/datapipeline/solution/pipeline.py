"""functions for transforming to results"""
import json
from collections import defaultdict
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

RACES_SCHEMA = "raceId INT, year INT, round INT, name STRING, date STRING, time STRING"
RESULTS_SCHEMA = "resultId INT, raceId INT, driverId INT, position INT, fastestLapTime STRING"


def read_csv(spark: SparkSession, path: str, schema: str) -> DataFrame:
    return spark.read.csv(path, header=True, schema=schema, nullValue="null")

def get_race_winners(results: DataFrame) -> DataFrame:
    return results.filter(F.col("position") == 1).select("raceId", "driverId")


def get_fastest_laps(results: DataFrame) -> DataFrame:
    #smallest string is the quickest lap
    return results.groupBy("raceId").agg(F.min("fastestLapTime").alias("fastestLap"))

def build_race_stats(races: DataFrame, results: DataFrame) -> DataFrame:
    # left joins so races without results yet are still included
    time = F.coalesce(F.col("time"), F.lit("00:00:00"))
    return (
        races.join(get_race_winners(results), on="raceId", how="left")
        .join(get_fastest_laps(results), on="raceId", how="left")
        .select(
            "year",
            F.col("name").alias("Race Name"),
            F.col("round").alias("Race Round"),
            F.concat(F.col("date"), F.lit("T"), time, F.lit(".000")).alias("Race Datetime"),
            F.col("driverId").alias("Race Winning driverId"),
            F.col("fastestLap").alias("Race Fastest Lap"),
        )
        .orderBy("year", "Race Round")
    )


def write_stats_by_year(race_stats: DataFrame, output_dir: str) -> None:
    races_by_year = defaultdict(list)
    for row in race_stats.collect():
        race = row.asDict()
        races_by_year[race.pop("year")].append(race)

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for year, races in races_by_year.items():
        with open(f"{output_dir}/stats_{year}.json", "w", encoding="utf-8") as f:
            json.dump(races, f, indent=4, ensure_ascii=False)


# ## Objective
# - Develop a data pipeline that produces JSON files which have the same structure as below.
# - Each element in the list should be for one race from the `races.csv` file.
# - You should produce one file per year available in the source data.
# - Your JSON files should be called `stats_{year}.json`, one for each year and be placed in the `results` folder. 
#   - For example for 2024, the file should be called `stats_2024.json`.
# - As an example for a 2024 race:
# ```
#   [
# 	  {
# 		  "Race Name": "British Grand Prix",
# 		  "Race Round": 12,
# 		  "Race Datetime": "2024-07-07T14:00:00.000",
# 		  "Race Winning driverId": 1,
# 		  "Race Fastest Lap": "01:29.4"
# 	  },
# 	  ...
#   ]
# ```

# - In `races.csv`, the `date` and `time` column are the date and time of the race.
# - In `races.csv`, all dates and times are in UTC
# - If the time is not available in `races.csv`, use `00:00:00`
# - In `results.csv` the winning driver is determined as the one who finished in position 1 for that race
# - If the JSON value for a key is always a number, represent it as such rather than a string
#