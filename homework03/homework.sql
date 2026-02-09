-- BigQuery Setup
CREATE OR REPLACE EXTERNAL TABLE `your-project.your_dataset.yellow_taxi_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_hw3_2025/yellow_tripdata_2024-*.parquet']
);

CREATE OR REPLACE TABLE `your-project.your_dataset.yellow_taxi_materialized` AS
SELECT * FROM `your-project.your_dataset.yellow_taxi_external`;


-- Question 1: Counting records
SELECT COUNT(*) as record_count
FROM `your-project.your_dataset.yellow_taxi_materialized`;


-- Question 2: Data read estimation
SELECT COUNT(DISTINCT PULocationID)
FROM `your-project.your_dataset.yellow_taxi_external`;

SELECT COUNT(DISTINCT PULocationID)
FROM `your-project.your_dataset.yellow_taxi_materialized`;

-- Question 3: Understanding columnar storage
SELECT PULocationID
FROM `your-project.your_dataset.yellow_taxi_materialized`;

SELECT PULocationID, DOLocationID
FROM `your-project.your_dataset.yellow_taxi_materialized`;

-- Question 4: Counting zero fare trips
SELECT COUNT(*) as zero_fare_count
FROM `your-project.your_dataset.yellow_taxi_materialized`
WHERE fare_amount = 0;

-- Question 5: Partitioning and clustering
CREATE OR REPLACE TABLE `your-project.your_dataset.yellow_taxi_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `your-project.your_dataset.yellow_taxi_materialized`;

-- Question 6: Partition benefits
SELECT DISTINCT VendorID
FROM `your-project.your_dataset.yellow_taxi_materialized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT VendorID
FROM `your-project.your_dataset.yellow_taxi_partitioned_clustered`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';



