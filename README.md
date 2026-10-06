\# ETL Airflow Project



\## Project Overview



Automated ETL pipeline that extracts customer data from a REST API, validates the data, loads it into PostgreSQL staging, performs incremental UPSERT processing, and records pipeline execution using audit logging. Apache Airflow orchestrates the complete workflow.



\## Architecture



REST API

↓

Extract

↓

Raw JSON

↓

Validate

↓

PostgreSQL Staging

↓

Incremental UPSERT

↓

Customers

↓

Audit Logging



\## Technologies



\- Python

\- PostgreSQL

\- Apache Airflow

\- Docker

\- Docker Compose

\- REST API

\- SQL

\- Git \& GitHub



\## Airflow Workflow



extract\_data

↓

validate\_data

↓

load\_to\_staging

↓

incremental\_load



\## Database Tables



\- staging\_customers

\- customers

\- pipeline\_audit



\## Features



\- REST API extraction

\- Data validation

\- PostgreSQL staging

\- Incremental loading

\- UPSERT processing

\- Error handling

\- Airflow retries

\- Audit logging

\- Dockerized Airflow



\## Validation Results



\- 10 records extracted

\- 10 records validated

\- 10 records loaded to staging

\- 10 records loaded to customers

\- Airflow pipeline completed successfully



\## How to Run



```bash

docker compose up -d airflow-webserver airflow-scheduler

