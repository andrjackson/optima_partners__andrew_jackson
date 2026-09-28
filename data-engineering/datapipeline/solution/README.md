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
# run one of the below based on os
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\Activate.ps1       # Windows PowerShell
pip install -r solution/requirements.txt
# run the actual pipeline
python solution/main.py
```

## How it works
All the logic is in `pipeline.py`. `main.py` just wires it together.

Tests run separately but could be run automatically via github actions in a proper CI/CD setup

## Running the tests
```bash
cd solution
python -m pytest
```
## Cloud Options
The databricks.yml file adds the functionality here to deploy this as a databricks asset bundle. Before doing so, some considerations would need to be made and cloud hosting established. I'll discuss launching this on an AWS/Databricks platform.
### Tools
- **Databricks Asset Bundles**: define the job, trigger, compute
- **Unity Catalog volumes**: hold the source CSVs and output JSON
- **S3 + Terraform**: the volume would sit on an S3 external location. The
  bucket, IAM role, storage credential and external location would be
  managed in Terraform as infrastructure
- **IAM Roles**: designed in conjunction with Databricks Permissions and Groups to define access to cloud data
### Considerations
- Prod and Dev data should sit in separate catalogs, inaccessible across environments
- All deployments should be via DABs for consistency - no deploying to prod without first testing in dev
- job failures should go to email and slack/teams, or to a monitoring system like Splunk if essential
- Permissions for data should be set at the minimum level in IAM and Databricks

## Challenges completed:
### Objective
- [x] Develop a data pipeline that produces JSON files which have the same structure as below.
- [x] Each element in the list should be for one race from the `races.csv` file.
- [x] You should produce one file per year available in the source data.
- [x] Your JSON files should be called `stats_{year}.json`, one for each year and be placed in the `results` folder. 
- [x] If the time is not available in `races.csv`, use `00:00:00`
- [x] In `results.csv` the winning driver is determined as the one who finished in position 1 for that race
- [x] If the JSON value for a key is always a number, represent it as such rather than a string

### Stretch goals
- [x] Include unit tests for all functions. NOTE: I didnt add unit tests for all them, only some examples
- [x] While this assignmment does not require you to deploy to a cloud provider, the solution would eventually require this. Add some notes to your documentation about the tools you might use to deploy this pipeline to a cloud provider of your choice and what kind of considerations you'd need to make in doing so. NOTE: I added a Databricks DAB deployment to demonstrate the scenario where this is deployed to the cloud, cloud agnostic through DBX

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
