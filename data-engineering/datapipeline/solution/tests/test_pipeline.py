import json

from pipeline import (
    RACES_SCHEMA,
    RESULTS_SCHEMA,
    build_race_stats,
    get_fastest_laps,
    get_race_winners,
    read_csv,
    write_stats_by_year,
)


def make_races(spark, rows):
    return spark.createDataFrame(rows, RACES_SCHEMA)


def make_results(spark, rows):
    return spark.createDataFrame(rows, RESULTS_SCHEMA)


def test_get_race_winners_only_keeps_position_one(spark):
    results = make_results(spark, [
        (1, 100, 44, 2, "01:30.0"),
        (2, 100, 1, 1, "01:31.0"),
        (3, 100, 16, None, None),
    ])

    winners = get_race_winners(results).collect()

    assert [(w["raceId"], w["driverId"]) for w in winners] == [(100, 1)]


def test_build_race_stats_output_format(spark):
    races = make_races(spark, [(1132, 2024, 12, "British Grand Prix", "2024-07-07", "14:00:00")])
    results = make_results(spark, [
        (1, 1132, 1, 1, "01:29.4"),
        (2, 1132, 830, 2, "01:29.0"),
    ])

    row = build_race_stats(races, results).first().asDict()

    assert row == {
        "year": 2024,
        "Race Name": "British Grand Prix",
        "Race Round": 12,
        "Race Datetime": "2024-07-07T14:00:00.000",
        "Race Winning driverId": 1,
        "Race Fastest Lap": "01:29.0",
    }