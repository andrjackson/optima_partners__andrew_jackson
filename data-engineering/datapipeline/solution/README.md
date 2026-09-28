# Solution README

## Description
A PySpark pipeline that reads source-data/races.csv and source-data/results.csv and writes one stats_{year}.json file per year into the results folder.

## Requirements
- Python 3.10+
- Java 17 (for PySpark)

## Running the pipeline
From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r solution/requirements.txt
python solution/main.py
```

## How it works
All the logic is in `pipeline.py`. `main.py` just wires it together.

## Running the tests
```bash
cd solution
python -m pytest
```

## Challenges completed:
### Objective
[x] Develop a data pipeline that produces JSON files which have the same structure as below.
[x] Each element in the list should be for one race from the `races.csv` file.
[x] You should produce one file per year available in the source data.
[x] Your JSON files should be called `stats_{year}.json`, one for each year and be placed in the `results` folder. 
[x] If the time is not available in `races.csv`, use `00:00:00`
[x] In `results.csv` the winning driver is determined as the one who finished in position 1 for that race
[x] If the JSON value for a key is always a number, represent it as such rather than a string

### Stretch goals
[x] Include unit tests for all functions. NOTE: I didnt add unit tests for all them, only some examples
[x] While this assignmment does not require you to deploy to a cloud provider, the solution would eventually require this. Add some notes to your documentation about the tools you might use to deploy this pipeline to a cloud provider of your choice and what kind of considerations you'd need to make in doing so. NOTE: I added a Databricks DAB deployment to demonstrate the scenario where this is deployed to the cloud, cloud agnostic through DBX

## Databricks Deploy
databricks.yml adds an option for deploying this as a Daatbricks Asset Bundle, including a job and volumes

**One-off setup**: create a volume and upload the source data. The default path is `/Volumes/main/f1/race_data` set in the .yml

create the schema and volume
```sql
CREATE SCHEMA IF NOT EXISTS main.f1;
CREATE VOLUME IF NOT EXISTS main.f1.race_data;
```

copy the data to the correct volume
```bash
databricks fs cp -r source-data dbfs:/Volumes/main/f1/race_data/source-data
```

The results lands in `/Volumes/main/f1/race_data/results/`. Use `-t prod` to deploy the production target, it will default to dev
