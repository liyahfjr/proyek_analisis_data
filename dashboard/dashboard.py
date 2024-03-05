import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='white')

st.header('Peminjaman Sepeda Dashboard :sparkles:')
st.subheader('Pengaruh Suhu terhadap Peminjaman Sepeda (6 Bulan Terakhir)')

day_hour_df = pd.read_csv("dashboard/all_data.csv")

day_hour_df['dteday'] = pd.to_datetime(day_hour_df['dteday'])
six_months_ago = day_hour_df['dteday'].max() - pd.DateOffset(months=6)
recent_data = day_hour_df[day_hour_df['dteday'] >= six_months_ago]

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    recent_data["temp_day"],
    recent_data["cnt_day"],
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader('Persentase Peningkatan Peminjaman Sepeda\n(Hari Kerja vs. Hari Libur)')

one_year_ago = day_hour_df['dteday'].max() - pd.DateOffset(years=1)
last_year_data = day_hour_df[day_hour_df['dteday'] >= one_year_ago]

weekday_counts = last_year_data.groupby('workingday_day')['cnt_day'].sum()

percentage_increase = ((weekday_counts[1] - weekday_counts[0]) / weekday_counts[0]) * 100

labels = ['Hari Kerja', 'Hari Libur']
sizes = [weekday_counts[1], weekday_counts[0]]
colors = ['lightblue', 'lightgreen']

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)

st.pyplot(fig)

st.subheader('Hubungan Kecepatan Angin terhadap Peminjaman Sepeda (Jam Sibuk, Hari Kerja)')

busy_hours_data = last_year_data[(last_year_data['hr'] >= 7) & (last_year_data['hr'] <= 19) & (last_year_data['workingday_day'] == 1)]

fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(busy_hours_data['windspeed_hour'], busy_hours_data['cnt_hour'])
ax.set_xlabel('Kecepatan Angin')
ax.set_ylabel('Jumlah Peminjaman')

st.pyplot(fig)

st.subheader('Persentase Peminjaman Sepeda di Berbagai Musim (Hari Kerja)')

season_workday_counts = day_hour_df[day_hour_df['workingday_day'] == 1].groupby('seasons')['cnt_day'].sum()

total_workday_counts = season_workday_counts.sum()

percentage_by_season = (season_workday_counts / total_workday_counts) * 100

fig, ax = plt.subplots(figsize=(10, 6))
percentage_by_season.plot(kind='bar', color=['lightblue', 'lightgreen', 'lightcoral', 'lightyellow'], ax=ax)
ax.set_xlabel('Musim')
ax.set_ylabel('Persentase Peminjaman')
ax.set_xticklabels(percentage_by_season.index, rotation=0)

st.pyplot(fig)
