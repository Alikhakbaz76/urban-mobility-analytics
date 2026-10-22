from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# ==========================================
# 1. Project Setup and Data Loading
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
file_path = PROJECT_ROOT / "data" / "raw" / "JC-202505-citibike-tripdata.csv"
REPORTS_PATH = PROJECT_ROOT / "reports"
REPORTS_PATH.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(file_path)
print("\n--- Dataset Shape ---",df.shape)
print("\n--- First 5 Rows ---",df.head())
print("\n--- Column Data Types ---" , df.dtypes)
print("\n--- Dataset Information ---")
df.info()

# ==========================================
# 2. Data Quality Checks
# ==========================================

missing_values = df.isna().sum()
missing_values_pct = missing_values / len(df) * 100
print("\n--- Missing Values Count ---")
print(missing_values[missing_values > 0].sort_values(ascending=False))
print("\n--- Missing Values Percentage ---")
print(missing_values_pct[missing_values_pct > 0]
      .sort_values(ascending=False)
      .round(4)
      )
print("\n--- Missing End Station Details ---")
missing_end_station = df[
    df['end_station_id'].isna() |
    df['end_station_name'].isna()
]

print(missing_end_station[
    ['end_station_id', 'end_station_name']
].shape)

print(missing_end_station[
    ['end_station_id', 'end_station_name']
].isna().sum())

print("\n--- Missing End Station Combinations ---")

both_missing = (
    df['end_station_id'].isna() &
    df['end_station_name'].isna()
).sum()

print("Both missing:", both_missing)

print(
    "Only ID missing:",
    (
        df['end_station_id'].isna() &
        df['end_station_name'].notna()
    ).sum()
)

print(
    "Only name missing:",
    (
        df['end_station_id'].notna() &
        df['end_station_name'].isna()
    ).sum()
)

print("\n--- Duplicate Ride ID Check ---")
duplicate_ride_ids = df['ride_id'].duplicated(keep=False)
print("Rows with duplicated ride IDs:", duplicate_ride_ids.sum())

duplicate_rows = df.duplicated().sum()
print("\n--- Duplicate Rows ---")
print(duplicate_rows)

# ==========================================
# 3. Trip Duration Analysis
# ==========================================

df['started_at'] = pd.to_datetime(df['started_at'])
df['ended_at'] = pd.to_datetime(df['ended_at'])
df['ride_duration'] = df['ended_at'] - df['started_at']

df['ride_duration_min'] = df['ride_duration'].dt.total_seconds() / 60
print("\n--- Trip Duration Statistics ---")

print(
    df['ride_duration_min'].describe().round(2)
)

q1 = df['ride_duration_min'].quantile(0.25)
q3 = df['ride_duration_min'].quantile(0.75)
iqr = q3 - q1 
Upper_Bound = q3 + 1.5 * iqr
print("Q1 : " , q1)
print("Q3 : " , q3)
print("IQR : " , iqr)
print("Upper_Bound:", Upper_Bound)

outlier_count = (df['ride_duration_min'] > Upper_Bound).sum()
print("Number of outliers:", outlier_count)

trips_up_to_60_min = (df['ride_duration_min'] <= 60 ).sum()
print("Trips Smaller Than 60 Minutes :", trips_up_to_60_min)

trips_over_60_min = (df['ride_duration_min'] > 60 ).sum()
print("Trips Longer Than 60 Minutes :", trips_over_60_min)

print("\n--- First 5 Trip Durations (minutes) ---")
print(df['ride_duration_min'].head())
print("\n--- Trip Share by User Type (%) ---")
print((df['member_casual'].value_counts(normalize=True) * 100).round(2))
print("\n--- Average Trip Duration (minutes) ---")
print((
   df.groupby('member_casual')['ride_duration_min'].mean().round(2))
)
print("\n--- Median Trip Duration (minutes) ---")
print((
     df.groupby('member_casual')['ride_duration_min'].median().round(2))
)
print("\n--- Standard Deviation of Trip Duration ---")
print((
     df.groupby('member_casual')['ride_duration_min'].std().round(2))
)

print("\n--- Trips with Non-positive Duration ---")
print((df['ride_duration_min'] <= 0).sum())

print("\n--- Maximum Trip Duration (minutes) ---")
print(df['ride_duration_min'].max())


df_under_60 = df.loc[
    df['ride_duration_min'] <= 60 ,
    ['ride_duration_min','member_casual']
]

print("\n--- Median Trip Duration: Trips Up to 60 Minutes ---")
print(
    df_under_60.groupby('member_casual')['ride_duration_min'].median().round(2)
)

print("\n--- Average Trip Duration: Trips Up to 60 Minutes ---")
print(
    df_under_60.groupby('member_casual')['ride_duration_min'].mean().round(2)
)

# ==========================================
# 4. Time-Based Analysis
# ==========================================

day_order = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday',
    'Friday', 'Saturday', 'Sunday'
]


df['started_at_day'] = df['started_at'].dt.day_name()
df['started_at_hour'] = df['started_at'].dt.hour

started_at_hour_corr = df[['started_at_hour','ride_duration_min']].corr()
print(started_at_hour_corr)

print(
    df.groupby('member_casual')[['started_at_hour','ride_duration_min']].corr()
)

avg_duration_by_hour = df.groupby(['member_casual','started_at_hour'])['ride_duration_min'].mean()
avg_duration_by_hour_unstack= avg_duration_by_hour.round(2).unstack()
ax = avg_duration_by_hour_unstack.plot(
    kind='bar',
    figsize=(10,5)
)
ax.set_title('Average Trip Duration by Hour and User Type')
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Average Trip Duration (minutes)')
ax.legend(
    title='User Type',
    loc='upper left',
    bbox_to_anchor=(1.02, 1)
)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "avg_duration_by_hour.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

avg_duration_by_day = df.groupby(['member_casual','started_at_day'])['ride_duration_min'].mean()
avg_duration_by_day_unstack= avg_duration_by_day.unstack()
avg_duration_by_day_unstack_ = avg_duration_by_day_unstack.reindex(columns= day_order)
ax = avg_duration_by_day_unstack_.plot(
    kind='bar',
    figsize=(10,5)
)
ax.set_title('Average Trip Duration by Day and User Type')
ax.set_xlabel('Day of Week')
ax.set_ylabel('Average Trip Duration (minutes)')
ax.legend(
    title='User Type',
    loc='upper left',
    bbox_to_anchor=(1.02, 1)
)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "avg_duration_by_day.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


hourly_trips = df.groupby(['member_casual','started_at_hour']).size()
total_hourly_trips_by_user_type = hourly_trips.groupby(level=0).transform('sum')
hourly_percentage = hourly_trips / total_hourly_trips_by_user_type  * 100
hourly_percentage_unstack = hourly_percentage.unstack(level=0)
print("\n--- Peak Trip Hour by User Type ---")
print(hourly_percentage_unstack.idxmax())
print("\n--- Highest Hourly Trip Share (%) ---")
print(hourly_percentage_unstack.max().round(2))


ax = hourly_percentage_unstack.plot(
    kind='line',
    marker='o',
    figsize=(10, 5)
)
ax.set_title('Hourly Trip Distribution by User Type')
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Share of Trips (%)')
ax.legend(title='User Type')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "hourly_trips_by_user_type.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

print(
    df['start_station_name'].value_counts().head(10)
)

station_shares = df.groupby('member_casual')['start_station_name'].value_counts(normalize=True) * 100
casual_top10= station_shares.loc['casual'].head(10)
member_top10 = station_shares.loc['member'].head(10)
station_comparison = pd.concat([member_top10 ,casual_top10], axis= 1 )
station_comparison.columns = ['member_percentage' , 'casual_percentage']
station_comparison = station_comparison.fillna(0)
station_comparison = station_comparison.sort_values(
    by='member_percentage',
    ascending=True
)
ax = station_comparison.plot(
    kind='barh',
    figsize=(10, 5)
)
ax.set_title('Top 10 Start Stations by User Type')
ax.set_xlabel('Percentage of Trips (%)')
ax.set_ylabel('Start Station')
ax.legend(title='User Type')
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "top_start_stations_by_user_type.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


station_shares_end = df.groupby('member_casual')['end_station_name'].value_counts(normalize=True) * 100
casual_end_top10 = station_shares_end.loc['casual'].head(10)
member_end_top10 = station_shares_end.loc['member'].head(10)
end_station_comparison = pd.concat([member_end_top10 , casual_end_top10],axis= 1)
end_station_comparison.columns = ['member_percentage' , 'casual_percentage']
end_station_comparison = end_station_comparison.fillna(0)
nd_station_comparison = end_station_comparison.sort_values(
    by='member_percentage',
    ascending=True
)

ax = nd_station_comparison.plot(
    kind='barh',
    figsize=(10, 5)
)
ax.set_title('Top 10 End Stations by User Type')
ax.set_xlabel('Percentage of Trips (%)')
ax.set_ylabel('End Station')
ax.legend(title='User Type')
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "top_end_stations_by_user_type.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


daily_trips = df.groupby(['member_casual','started_at_day']).size()
total_daily_trips_by_user_type = daily_trips.groupby(level=0).transform('sum')
daily_trip_percentage = daily_trips / total_daily_trips_by_user_type * 100
daily_trip_percentage_wide = daily_trip_percentage.unstack()

daily_trip_percentage_wide = daily_trip_percentage_wide.reindex(
    columns=day_order
)
ax = daily_trip_percentage_wide.plot(
    kind='bar',
    figsize=(10, 5)
)
ax.set_title('Trip Distribution by Day of Week and User Type')
ax.set_xlabel('Day of Week')
ax.set_ylabel('Percentage of Trips (%)')
ax.legend(title='User Type')
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "daily_trips_by_weekday.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


duration_stats = df.groupby('member_casual')['ride_duration_min'].agg(
    ['mean' , 'median' , 'std']
)
print(duration_stats.round(2))
trips_up_to_60_min_2 = df[df['ride_duration_min'] <= 60]
duration_stats_up_to_60_min = trips_up_to_60_min_2.groupby('member_casual')['ride_duration_min'].agg(
    ['mean' , 'median' , 'std']
)
print(duration_stats_up_to_60_min.round(2))

print(
    df.groupby('rideable_type')['ride_duration_min'].agg(['mean' , 'median' , 'std']
                         ).round(2)
)
fig , ax = plt.subplots(figsize =(10,5))

sns.boxplot(
    data = df,
    x='rideable_type',
    y='ride_duration_min',
    ax=ax
)
ax.set_title('Trip Duration by Bike Type')
ax.set_xlabel('Bike Type')
ax.set_ylabel('Trip Duration (minutes)')    
ax.set_ylim(0, 30)                   
plt.tight_layout()
plt.savefig(REPORTS_PATH / 'trip_duration_by_bike_type.png',
            dpi=300, bbox_inches='tight')                        
plt.show()   


fig , ax = plt.subplots(figsize = (10 , 5))
sns.boxplot(
    data= trips_up_to_60_min_2,
    x='rideable_type',
    y='ride_duration_min',
    ax = ax    
    
)
ax.set_title('Trip Duration by Bike Type (Trips ≤ 60 Minutes)')
ax.set_xlabel('Bike Type')
ax.set_ylabel('Trip Duration (Minutes)')    
ax.set_ylim(0, 30)                   
plt.tight_layout()
plt.savefig(REPORTS_PATH / 'trip_duration_by_bike_type_under_60_min.png',
            dpi=300, bbox_inches='tight')                        
plt.show()   

                     
# ==========================================
# 5. Bike Type Analysis
# ==========================================

bike_type_counts = df.groupby(['member_casual' , 'rideable_type']).size()
total_bike_trips_by_user_type = bike_type_counts.groupby(level=0).transform('sum')
bike_type_percentage = (
    bike_type_counts / total_bike_trips_by_user_type * 100
)
bike_type_percentage_wide = bike_type_percentage.unstack()
ax = bike_type_percentage_wide.plot(
    kind='bar',
    figsize=(10, 5)
)
ax.set_title('Bike Type Usage by User Type')
ax.set_xlabel('User Type')
ax.set_ylabel('Percentage of Trips (%)')
ax.legend(title='Bike Type')
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "bike_type_by_user_type.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()




print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print(df.info())
print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
