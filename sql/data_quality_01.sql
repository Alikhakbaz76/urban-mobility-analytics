-- Project: Urban Mobility Analytics
-- Description: SQL analysis of bike-sharing trip data.
-- Purpose: Explore data quality, user behavior, trip duration,
-- hourly and daily demand, bike types, and popular stations.



-- 1. Check total rows
-- This establishes the size of the dataset.

SELECT COUNT(*)
FROM bike_trips_clean;

-- 2. Check whether ride IDs are unique
-- Compare total records with distinct ride IDs to identify potential duplicates.

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT ride_id) AS unique_rides
FROM bike_trips_clean;

-- 3. Check missing end station names
-- Calculate the number and percentage of trips without an end station name.

SELECT
    COUNT(*) AS total_rows,
    COUNT(end_station_name) AS filled_end_stations,
    COUNT(*) - COUNT(end_station_name) AS missing_end_stations,
    ROUND(
        100.0 * (COUNT(*) - COUNT(end_station_name)) / COUNT(*),
        2
    ) AS missing_percentage
FROM bike_trips_clean;

-- 4. Count trips by user type
-- Compare the total number of trips made by members and casual users.
SELECT
    member_casual,
    COUNT(*) AS total_trips
FROM bike_trips_clean
GROUP BY member_casual
ORDER BY total_trips DESC;

-- 5.  Calculate trip counts and percentages by user type
-- Measure each user group's share of all trips.
SELECT
    member_casual,
    COUNT(*) AS total_trips,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS trip_percentage
FROM bike_trips_clean
GROUP BY member_casual
ORDER BY total_trips DESC;

-- 6.  Calculate average trip duration by user type
-- Compare the average ride duration of members and casual users.
SELECT
    member_casual,
    COUNT(*) AS total_trips,
    ROUND(
        AVG(
            EXTRACT(EPOCH FROM (ended_at - started_at)) / 60.0
        )::numeric,
        2
    ) AS avg_duration_min
FROM bike_trips_clean
GROUP BY member_casual
ORDER BY avg_duration_min DESC;


-- 7.  Calculate the percentage of trips longer than 60 minutes
-- Identify how many trips exceed one hour and their share of all trips.
SELECT
    COUNT(*) AS total_trips,
    COUNT(*) FILTER(
WHERE ended_at - started_at > INTERVAL '60 minutes' 
	)AS trips_over_60_min,
	ROUND( 100.0 * COUNT(*) FILTER(
WHERE ended_at - started_at > INTERVAL '60 minutes') / COUNT(*),2) AS percentage_over_60_min
FROM bike_trips_clean;

-- 8. Trip count by day of week
-- Use PostgreSQL DOW values: Sunday = 0, Monday = 1, ..., Saturday = 6

SELECT  EXTRACT(DOW FROM started_at) AS day_of_week 
 , COUNT (*) AS trip_count
    FROM bike_trips_clean 
GROUP BY day_of_week
ORDER BY day_of_week;


-- 9. Calculate the percentage of Saturday trips made by casual users
-- Examine the share of casual users among all Saturday trips
SELECT
    ROUND(
        (
            100.0 * COUNT(*) FILTER (
                WHERE member_casual = 'casual'
            ) / COUNT(*)
        )::numeric,
        2
    ) AS casual_percentage
FROM bike_trips_clean
WHERE EXTRACT(DOW FROM started_at) = 6;

-- 10. Trip count by hour and user type
-- Compare hourly trip volumes for members and casual users
SELECT
    member_casual,
    EXTRACT(HOUR FROM started_at) AS trip_hour,
    COUNT(*) AS trip_count
FROM bike_trips_clean
GROUP BY member_casual, trip_hour
ORDER BY trip_count DESC;


-- 11.  Identify the peak trip hour for each user type
-- RANK returns the busiest hour or hours, including ties

WITH ranked_trips AS (
    SELECT
        member_casual,
        EXTRACT(HOUR FROM started_at) AS trip_hour,
        COUNT(*) AS trip_count,
        RANK() OVER (
            PARTITION BY member_casual
            ORDER BY COUNT(*) DESC
        ) AS hour_rank
    FROM bike_trips_clean
    GROUP BY member_casual, trip_hour
)
SELECT *
FROM ranked_trips
WHERE hour_rank = 1
ORDER BY member_casual;


-- 12. Identify the least busy trip hour for each user type.
-- RANK returns the quietest hour or hours, including ties.

WITH ranked_trips AS (
    SELECT
    member_casual,
    EXTRACT(HOUR FROM started_at) AS trip_hour,
    COUNT(*) AS trip_count,
    RANK() OVER (
        PARTITION BY member_casual
        ORDER BY COUNT(*) asc
    ) AS hour_rank
FROM bike_trips_clean
GROUP BY member_casual, trip_hour
)
SELECT *
FROM ranked_trips
WHERE hour_rank = 1
ORDER BY member_casual;


-- 13. Calculate the gap between peak and least busy hours
-- Compare the highest and lowest hourly trip counts for each user type.

WITH ranked_trips AS (
    SELECT
        member_casual,
        EXTRACT(HOUR FROM started_at) AS trip_hour,
        COUNT(*) AS trip_count,

        RANK() OVER (
            PARTITION BY member_casual
            ORDER BY COUNT(*) DESC
        ) AS peak_rank,

        RANK() OVER (
            PARTITION BY member_casual
            ORDER BY COUNT(*) ASC
        ) AS quiet_rank

    FROM bike_trips_clean
    GROUP BY member_casual, trip_hour
),

trip_extremes AS (
    SELECT
        member_casual,

        CASE
            WHEN peak_rank = 1 THEN trip_count
        END AS peak_trip_count,

        CASE
            WHEN quiet_rank = 1 THEN trip_count
        END AS quiet_trip_count

    FROM ranked_trips
    WHERE quiet_rank = 1 OR peak_rank = 1
)

SELECT
    member_casual,
    MAX(peak_trip_count) AS peak_trip_count,
    MAX(quiet_trip_count) AS quiet_trip_count,
    MAX(peak_trip_count) - MAX(quiet_trip_count) AS trip_count_gap

FROM trip_extremes
GROUP BY member_casual
ORDER BY member_casual;


-- 14. Calculate electric bike usage by user type.
-- Compare the percentage of trips made using electric bikes.

SELECT
    member_casual,
    COUNT(*) AS total_trips,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE rideable_type = 'electric_bike'
        ) / COUNT(*), 2
    ) AS electric_bike_pct
FROM bike_trips_clean
GROUP BY member_casual;


-- 15. Calculate average trip duration by user type and bike type.
-- Compare ride durations for classic and electric bikes within each user group.

WITH trip_durations AS(
 SELECT member_casual,rideable_type,(ended_at - started_at) AS trip_duration
 FROM bike_trips_clean

)
SELECT member_casual,rideable_type ,ROUND (
    (AVG(EXTRACT(EPOCH FROM trip_duration)) / 60.0)::numeric,2) AS avg_duration_minutes
FROM trip_durations
GROUP BY member_casual , rideable_type;



-- 16. Calculate average daily trips by user type and day category.
-- Compare weekday and weekend demand using the number of dates with recorded trips.

WITH trips AS (
    SELECT
        member_casual,
        COUNT(*) AS total_trips,
        CASE
            WHEN EXTRACT(ISODOW FROM started_at) IN (6, 7)
                THEN 'Weekend'
            ELSE 'Weekday'
        END AS day_type
    FROM bike_trips_clean
    GROUP BY member_casual, day_type
),
days AS (
    SELECT
        CASE
            WHEN EXTRACT(ISODOW FROM started_at) IN (6, 7)
                THEN 'Weekend'
            ELSE 'Weekday'
        END AS day_type,
        COUNT(DISTINCT started_at::date) AS day_count
    FROM bike_trips_clean
    GROUP BY day_type
)
SELECT
    trips.member_casual,
    trips.day_type,
    trips.total_trips,
    ROUND(
        trips.total_trips::numeric / days.day_count,
        2
    ) AS avg_daily_trips
FROM trips
JOIN days USING (day_type)
ORDER BY trips.member_casual, trips.day_type;


-- 17. Calculate monthly trip percentages by user type.
-- Compare each group's share of monthly trips.

WITH monthly_trips AS (
select member_casual , 
DATE_TRUNC('month', started_at) AS trip_month,count(*) AS total_trips
from bike_trips_clean
group by trip_month ,member_casual
)
SELECT trip_month,
   (ROUND(100.0 * SUM(total_trips)FILTER(WHERE  member_casual = 'member') / SUM(total_trips) ,2))
    AS member_pct,
    (ROUND(100.0 * SUM(total_trips)FILTER(WHERE member_casual = 'casual') / SUM(total_trips) ,2))
     AS casual_pct
FROM monthly_trips
GROUP BY trip_month
ORDER BY trip_month;


-- 18. Identify the top 10 start stations by user type.
-- Rank stations by trip count separately for members and casual users.

WITH station_counts AS (
select member_casual , start_station_name ,count(*) AS total_trips
from bike_trips_clean
group by start_station_name , member_casual
),
station_ranks AS (
SELECT member_casual, start_station_name,total_trips ,(RANK() OVER (PARTITION BY member_casual ORDER BY total_trips DESC)) AS station_rank 
FROM station_counts
)
SELECT station_rank , member_casual, start_station_name,total_trips
FROM station_ranks
WHERE station_rank <= 10
ORDER BY member_casual, station_rank;