SELECT COUNT(*)
FROM fct_monthly_zone_revenue;


SELECT zone_name, SUM(revenue_monthly_total_amount) as total_revenue
FROM fct_monthly_zone_revenue
WHERE service_type = 'Green'
  AND EXTRACT(YEAR FROM revenue_month) = 2020
GROUP BY zone_name
ORDER BY total_revenue DESC
LIMIT 1;



SELECT SUM(total_monthly_trips)
FROM fct_monthly_zone_revenue
WHERE service_type = 'Green'
  AND revenue_month = '2019-10-01';


