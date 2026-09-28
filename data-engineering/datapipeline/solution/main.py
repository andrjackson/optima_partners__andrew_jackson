import argparse
from pathlib import Path

from pyspark.sql import SparkSession

from pipeline import (
    RACES_SCHEMA,
    RESULTS_SCHEMA,
    build_race_stats,
    read_csv,
    write_stats_by_year,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    # Defaults are the local repo folders. If this were running on databricks it would use
    # Unity Catalog volume paths instead. I've defined these in the databricks.yml as an example.
    parser = argparse.ArgumentParser(description="Build yearly F1 race stats JSON files.")
    args = parser.parse_args()

    spark = SparkSession.builder.appName("f1-race-stats").getOrCreate()

    races = read_csv(spark, f"{args.source_dir}/races.csv", RACES_SCHEMA)
    results = read_csv(spark, f"{args.source_dir}/results.csv", RESULTS_SCHEMA)

    write_stats_by_year(build_race_stats(races, results), args.output_dir)
    print(f"Wrote stats files to {args.output_dir}")


if __name__ == "__main__":
    main()