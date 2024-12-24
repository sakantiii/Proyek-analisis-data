import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

st.cache_data.clear()

sns.set(style='dark')

# Load the dataset
data = pd.read_csv("/mount/src/proyek-analisis-data/dashboard/all_data.csv")

# Ensure 'dteday' is a datetime column
data['dteday'] = pd.to_datetime(data['dteday'])

# Title
st.title("Bike Rental Dashboard :bike:")

# Sidebar for date filtering
min_date = data['dteday'].min()
max_date = data['dteday'].max()

with st.sidebar:
    st.header("Filters")
    start_date, end_date = st.date_input(
        label='Select Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data based on date range
filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) &
                     (data['dteday'] <= pd.to_datetime(end_date))]

# Daily Rentals Summary
daily_summary = filtered_data.groupby('dteday').agg(
    casual_rentals=('casual', 'sum'),
    registered_rentals=('registered', 'sum'),
    total_rentals=('cnt', 'sum')
).reset_index()

# Metrics
st.header("Overview")
total_rentals = daily_summary['total_rentals'].sum()
total_casual = daily_summary['casual_rentals'].sum()
total_registered = daily_summary['registered_rentals'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rentals", value=f"{total_rentals:,}")
with col2:
    st.metric("Casual Rentals", value=f"{total_casual:,}")
with col3:
    st.metric("Registered Rentals", value=f"{total_registered:,}")

# Daily Rentals Plot
st.subheader("Daily Rentals")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_summary['dteday'], daily_summary['casual_rentals'], label='Casual', marker='o', color='#90CAF9')
ax.plot(daily_summary['dteday'], daily_summary['registered_rentals'], label='Registered', marker='o', color='#FFB74D')
ax.plot(daily_summary['dteday'], daily_summary['total_rentals'], label='Total', marker='o', color='#4CAF50')

ax.set_title("Daily Rentals Over Time", fontsize=16)
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Number of Rentals", fontsize=12)
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)
plt.show()
plt.show()

# Frequent rental weekend and weekday
data['day_list'] = data['workingday'].map({1: 'Weekday', 0: 'Weekend'})
weekday_workingday = data.groupby('day_list').agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum" 
}).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(weekday_workingday['day_list'], weekday_workingday['casual'], color='steelblue', label='Casual')
ax.bar(weekday_workingday['day_list'], weekday_workingday['registered'], bottom=weekday_workingday['casual'], color='lightblue', label='Registered')
ax.set_title('Total Rental Based on weekend and weekday trend', fontsize=16)
ax.set_xlabel('day type', fontsize=12)
ax.set_ylabel('total count', fontsize=12)
ax.legend(title='Rental_type')
st.pyplot(fig)

# Rentals by Weather Condition
st.subheader("Rentals by Weather Condition")
weather_summary = filtered_data.groupby('weathersit').agg(
    total_rentals=('cnt', 'sum')
).reset_index().sort_values(by='total_rentals', ascending=False)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(
    x='total_rentals', 
    y='weathersit', 
    data=weather_summary, 
    palette='coolwarm', 
    ax=ax
)
ax.set_title("Total Rentals by Weather Condition", fontsize=16)
ax.set_xlabel("Total Rentals", fontsize=12)
ax.set_ylabel("Weather Condition", fontsize=12)
plt.show()
st.pyplot(fig)

# Hourly Analysis (if needed)
if 'hr' in data.columns:
    st.subheader("Hourly Rentals Distribution")
    hourly_summary = filtered_data.groupby('hr').agg(
        average_rentals=('cnt', 'mean')
    ).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        x='hr', 
        y='average_rentals', 
        data=hourly_summary, 
        marker='o', 
        ax=ax
    )
    ax.set_title("Average Hourly Rentals", fontsize=16)
    ax.set_xlabel("Hour", fontsize=12)
    ax.set_ylabel("Average Rentals", fontsize=12)
    plt.show()
    st.pyplot(fig)

st.caption('Dashboard created using Streamlit :sparkles:')
