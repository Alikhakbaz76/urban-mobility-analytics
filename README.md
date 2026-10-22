# Urban Mobility Analytics

## Project Overview

This project explores urban bike-sharing trip data to identify patterns in ride behavior, user types, trip duration, bike preferences, and station usage.

The analysis focuses on comparing casual riders and annual members to better understand how their riding patterns differ across time, bike types, and station locations.

The project uses Python for data analysis and visualization, with an emphasis on data quality, exploratory data analysis (EDA), and communicating actionable insights.

## Business Questions
This project aims to answer the following questions:

- How do trip durations differ between casual riders and annual members?
- How do riding patterns vary by day of the week and hour of the day?
- Which bike types are most commonly used by each user group?
- Which start and end stations are most frequently used by each group?
- How do trip duration patterns differ between classic bikes and electric bikes?

## Dataset
The analysis uses the Citi Bike trip dataset for May 2025.

- Source file: JC-202505-citibike-tripdata.csv
- Number of records: 93,227 trips
- Number of original columns: 13
- Data type: Bike-sharing trip records

The dataset includes information about ride IDs, bike types, trip start and end times, station names and IDs, station coordinates, and rider membership types.


## Tools & Technologies

- Python — Data analysis and processing
- Pandas — Data manipulation, aggregation, and cleaning
- Matplotlib — Data visualization
- Seaborn — Statistical data visualization
- VS Code — Development environment
- Git & GitHub — Version control and project sharing
- SQL — Data analysis and aggregation
- PostgreSQL — Relational database and query execution

## Data Cleaning & Preparation

The following data quality checks and preparation steps were performed:

- Inspected the dataset structure, column names, and data types.
- Checked missing values across all columns.
- Checked for duplicate rows and duplicate ride IDs.
- Converted trip start and end timestamps to datetime format.
- Calculated trip duration in minutes using the start and end timestamps.
- Identified non-positive trip durations.
- Investigated unusually long trips and potential outliers using the Interquartile Range (IQR) method.
- Created a filtered dataset of trips lasting 60 minutes or less for sensitivity analysis.

Long trips were retained in the primary analysis because unusually long durations are not necessarily invalid. The filtered dataset was used to examine how long trips affect summary statistics.

## Exploratory Data Analysis (EDA)

The exploratory data analysis focused on understanding ride patterns across user groups, time periods, bike types, and station locations.

1. User Type Analysis
- Compared the number of trips made by casual riders and annual members.
- Compared mean and median trip durations between user groups.
- Examined how long trips affect average duration and standard deviation.

2. Temporal Analysis
- Analyzed trip counts by hour of the day.
- Compared daily trip patterns across weekdays.
- Examined average trip duration by hour and day of the week.

3. Bike Type Analysis
- Compared classic bike and electric bike usage across user groups.
- Examined trip duration distributions by bike type.
- Used boxplots to investigate the distribution of trip durations and potential outliers.

4. Station Analysis
- Identified the most frequently used start stations for each user group.
- Identified the most frequently used end stations for each user group.
- Compared station usage percentages between casual riders and annual members.

5. SQL Analysis
- Compared trip volumes and percentages across user types.
- Analyzed trip patterns by hour and day of the week.
- Compared electric and classic bike usage across rider groups.
- Examined average daily trips on weekdays and weekends.
- Identified the most frequently used start stations by user type.
- Analysis of the percentage of Saturday trips made by casual riders.

## Key Findings

1. User Type Distribution
- Annual members accounted for approximately 74.9% of all trips.
- Casual riders accounted for approximately 25.1% of all trips.

2. Trip Duration
- Casual riders had a higher average trip duration (16.96 minutes) than annual  members (8.56 minutes).
- The median trip duration was 8.60 minutes for casual riders and 5.68 minutes for annual members.
- After filtering trips to 60 minutes or less, average trip duration decreased for both groups, while median duration changed only slightly. This indicates that long trips strongly influence the mean.

3. Riding Patterns
- Both user groups had the highest number of trips around 5 PM (17:00).
- Casual riders had a larger share of trips on weekends, particularly Saturdays.
- Annual members had a more weekday-oriented pattern, with Thursday and Friday accounting for relatively high shares of their trips.

4. Bike Type Preferences
- Electric bikes represented approximately 70.0% of casual riders' trips.
- Electric bikes represented approximately 59.4% of annual members' trips.
- Classic bike trips had a higher mean duration than electric bike trips, although the difference in median duration was much smaller.

5. Station Usage
- Hoboken Terminal - River St & Hudson Pl was among the most frequently used start stations for both groups.
- Grove St PATH represented a larger share of members' trips as an end station than casual riders' trips.
- Station usage patterns differed between casual riders and annual members, suggesting differences in how the two groups use the bike-sharing system.


## Visualizations
Hourly Trips by User Type

Daily Trips by Weekday

Bike Type by User Type

Average Trip Duration by Hour

Average Trip Duration by Day

Trip Duration by Bike Type

Trip Duration by Bike Type — Trips Up to 60 Minutes

Top Start Stations by User Type

Top End Stations by User Type

## Project Structure

urban-mobility-analytics/
├── data/
│   └── raw/
│       └── JC-202505-citibike-tripdata.csv
├── reports/
│   ├── hourly_trips_by_user_type.png
│   ├── daily_trips_by_weekday.png
│   ├── bike_type_by_user_type.png
│   ├── avg_duration_by_hour.png
│   ├── avg_duration_by_day.png
│   ├── trip_duration_by_bike_type.png
│   ├── trip_duration_by_bike_type_under_60_min.png
│   ├── top_start_stations_by_user_type.png
│   └── top_end_stations_by_user_type.png
├── sql/
│   └── data_quality_01.sql
├── src/
│  └── data_understanding_1.py
│
├──README.md
│
└──requirements.txt


## Folder Description

- data/raw/ — Contains the original trip dataset.
- src/ — Contains the Python analysis script.
- reports/ — Stores the visualizations generated during the analysis.
- README.md — Documents the project, methodology, and findings.

## How to Run
1. Clone the Repository

git clone <your-repository-url>
cd urban-mobility-analytics

2. Install Dependencies

Make sure Python is installed, then install the required libraries:

python -m pip install -r requirements.txt

3. Run the Analysis

Run the analysis script from the project root directory:

python src/data_understanding_1.py

The script reads the Citi Bike dataset, performs data quality checks and exploratory data analysis (EDA), and generates visualizations in the reports/ directory.

Note: Make sure the dataset is available at data/raw/JC-202505-citibike-tripdata.csv before running the script.

## Limitations & Future Improvements

# Limitations
The analysis covers only one month of Citi Bike trip data (May 2025), so the findings may not represent seasonal or year-round patterns.
The analysis is descriptive and does not establish causal relationships between rider type, trip duration, bike type, and station usage.
Unusually long trips may influence average trip durations and other summary statistics.
Missing station information may affect station-level comparisons.

# Future Improvements
Analyze multiple months of data to identify seasonal and long-term trends.
Build an interactive dashboard using tools such as Tableau, Power BI, or Plotly.
Perform statistical hypothesis tests to investigate differences between rider groups.
Explore station-level demand patterns and bike availability.
Develop predictive models for trip demand forecasting.

## SQL Validation

The SQL results were compared with the Python analysis to verify consistency across key data quality and exploratory analysis metrics.

### Validation Results

|               Metric            | Python Result | SQL Result |
|---------------------------------|---------------|------------|
|            Total trips          |     93,227    |   93,227   |
|          Unique ride IDs        |     93,227    |   93,227   |
|     Missing end station names   |       293     |    293     |
|      Missing end station IDs    |       350     |    350     |
|       Average trip duration     |    10.67 min  |  10.67 min |
|        Median trip duration     |    6.28 min   |   6.28 min |
|    Non-positive trip durations  |        0      |      0     |
|    Trips longer than 60 minutes |      1,251    |    1,251   |
|    Trips of 60 minutes or less  |      91,976   |    91,976  |
| Peak start hour for casual users|      17:00    |    17:00   |
|   Peak start hour for members   |      17:00    |    17:00   |
|         Member trip share       |      74.93%   |    74.93%  |
|         Casual trip share       |      25.07%   |    25.07%  |

### Conclusion

All metrics listed above matched between the Python analysis and SQL queries. This supports the consistency of the results for the checks performed. It does not imply that every column or every analysis query has been independently validated.