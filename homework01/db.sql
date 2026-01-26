
-- Q3. Counting short trips (<= 1 mile)

SELECT COUNT(*) AS trips_le_1_mile
FROM green_tripdata
WHERE lpep_pickup_datetime >= TIMESTAMP '2025-11-01'
  AND lpep_pickup_datetime <  TIMESTAMP '2025-12-01'
  AND trip_distance <= 1;


-- Q4. Longest trip day (trip_distance < 100)

SELECT DATE(lpep_pickup_datetime) AS pickup_day
FROM green_tripdata
WHERE lpep_pickup_datetime >= TIMESTAMP '2025-11-01'
  AND lpep_pickup_datetime <  TIMESTAMP '2025-12-01'
  AND trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;


-- Q5. Biggest pickup zone by total_amount on 2025‑11‑18

SELECT z."Zone" AS pickup_zone,
       SUM(g.total_amount) AS total_amount_sum
FROM green_tripdata g
JOIN zones z
  ON g."PULocationID" = z."LocationID"
WHERE g.lpep_pickup_datetime >= TIMESTAMP '2025-11-18'
  AND g.lpep_pickup_datetime <  TIMESTAMP '2025-11-19'
GROUP BY z."Zone"
ORDER BY total_amount_sum DESC
LIMIT 1;


-- Q6. Largest tip: PU zone = "East Harlem North" (Nov 2025), find DO zone

SELECT z_do."Zone" AS dropoff_zone,
       MAX(g.tip_amount) AS max_tip
FROM green_tripdata g
JOIN zones z_pu
  ON g."PULocationID" = z_pu."LocationID"
JOIN zones z_do
  ON g."DOLocationID" = z_do."LocationID"
WHERE g.lpep_pickup_datetime >= TIMESTAMP '2025-11-01'
  AND g.lpep_pickup_datetime <  TIMESTAMP '2025-12-01'
  AND z_pu."Zone" = 'East Harlem North'
GROUP BY z_do."Zone"
ORDER BY max_tip DESC
LIMIT 1;
