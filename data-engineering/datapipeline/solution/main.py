from pathlib import Path

from pipeline import (
    RACES_SCHEMA,
    RESULTS_SCHEMA,
    build_race_stats,
    create_spark_session,
    read_csv,
    write_stats_by_year,
)

#  datapipeline/ is the target of pipeline_dir
PIPELINE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = PIPELINE_DIR / "source-data"
RESULTS_DIR = PIPELINE_DIR / "results"


def main() -> None:
    spark = create_spark_session("f1-race-stats")
    try:
        races = read_csv(spark, str(SOURCE_DIR / "races.csv"), RACES_SCHEMA)
        results = read_csv(spark, str(SOURCE_DIR / "results.csv"), RESULTS_SCHEMA)
        stats = build_race_stats(races, results)
        write_stats_by_year(stats, RESULTS_DIR)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()