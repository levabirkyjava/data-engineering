
-- 3
SELECT COUNT(*) as total_rows
FROM public.yellow_tripdata
WHERE filename LIKE 'yellow_tripdata_2020%';

-- 4
SELECT COUNT(*) as total_rows
FROM public.green_tripdata
WHERE filename LIKE 'green_tripdata_2020%';

-- 5
CT 'Question 5: Yellow 2021-03', COUNT(*)
FROM public.yellow_tripdata
WHERE filename = 'yellow_tripdata_2021-03.csv';