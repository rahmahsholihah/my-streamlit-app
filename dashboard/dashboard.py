
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
sns.set(style='dark')

#DATA DAILY USERS
def create_daily_users_df(daily_bike_df): #DAILY ORDER
    daily_users_df = daily_bike_df.resample(rule="D", on="dteday").agg({ #mengelompokkan data dalam DataFrame berdasarkan tanggal menjadi kelompok-kelompok harian.
        "instant": "nunique", #Menghitung jumlah unik D pada setiap hari, yang artinya menghitung
        "casual" : "sum",
        "registered" : "sum",
        "cnt": "sum" #menjumlahkan total pengguna sepeda setiap hari.
    })
    daily_users_df = daily_users_df.reset_index() #Setelah proses agregasi, indeks DataFrame di-reset 
    daily_users_df.rename(columns={ #Nama kolom diubah agar lebih mudah dipahami,
        "casual" : "Casual Users",
        "registered" : "Registered Users",
        "cnt": "Total Users"
    }, inplace=True) #objek data asli akan dimodifikasi tanpa perlu membuat salinan baru dari objek tersebut.
    
    return daily_users_df #engembalikan DataFrame baru yang berisi informasi sewaan harian, yaitu tanggal dan jumlah penyewa setiap hari.

#DAILYWEEK USERS
def create_rentday_users_df(daily_bike_df): #rentday ORDER
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    daily_bike_df["rent_day"] = daily_bike_df["weekday"].map(lambda x: day_names[x])
    daily_bike_df.groupby("rent_day").dteday.nunique().sort_values(ascending=False)
    rentday_users_df = daily_bike_df.groupby(by="rent_day").agg({
    "casual": ["mean"],
    "registered": ["mean"],
}).sort_values(by=[("registered", "mean")], ascending=False).round(0)
    return rentday_users_df

#SEASONLY USERS
def create_seasonly_users_df(daily_bike_df): #SEASONLY ORDER
    daily_bike_df["season_name"] = daily_bike_df.season.apply(lambda x: "Spring" if x == 1 else ("Summer" if x == 2 else ("Fall" if x == 3 else "Winter")))
    seasonly_users_df = daily_bike_df.groupby(by="season_name").agg({
        "casual" : "mean",
        "registered" : "mean",
}).sort_values(by="registered", ascending=False)
    return seasonly_users_df

#WEATHERLY USERS
def create_weatherly_users_df(daily_bike_df):
    daily_bike_df["weather_type"] = daily_bike_df.weathersit.apply(lambda x: "Clear, Few clouds, Partly cloudy, Partly cloudy" if x == 1 else ("Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist" if x == 2 else ("Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds" if x == 3 else "Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog")))
    weatherly_users_df = daily_bike_df.groupby(by="weather_type").agg({
        "casual" : "mean",
        "registered" : "mean",
}).sort_values(by="registered", ascending=False)
    return weatherly_users_df

#MONTHYL USERS
def create_monthly_users_df(daily_bike_df):
    daily_bike_df["month_name"] = daily_bike_df["dteday"].dt.month_name()
    monthly_users_df = daily_bike_df.groupby(by="month_name").agg({
    "casual": "sum",
    "registered": "sum"
}).round(0).sort_values(by="registered", ascending=False)
    return monthly_users_df

#WEEKLY USERS
def create_weekly_users_df(daily_bike_df):
    daily_bike_df["rent_day"] = daily_bike_df.weekday.apply(lambda x: "Monday" if x == 0 else ("Tuesday" if x == 1 else ("Wednesday" if x == 2 else ("Thursday" if x == 3 else ("Friday" if x == 4 else ("Saturday" if x == 5 else "Sunday"))))))
    weekly_users_df = daily_bike_df.groupby(by="rent_day").agg({
        "casual" : "mean",
        "registered" : "mean"
}).round(0).sort_values(by="registered", ascending=False)
    return weekly_users_df

#WORK-HOLIDAY
def create_workholiday_users_df(daily_bike_df):
    daily_bike_df["day_type"] = daily_bike_df.workingday.apply(lambda x: "Work Day" if x == 1 else "Holiday")
    workholiday_users_df = daily_bike_df.groupby('day_type').agg({
        "casual" : "mean",
        "registered" : "mean"
})
    return workholiday_users_df

#CORRELATION
def create_atmosfer_df(daily_bike_df):
    atmosfer_df = daily_bike_df[["hum", "temp", "windspeed", "cnt"]]
    return atmosfer_df

#MEMBACA DATA
daily_bike_df = pd.read_csv("C:/Users/rahma/submission/data/day.csv")#LOAD DATA
hourly_bike_df = pd.read_csv("C:/Users/rahma/submission/data/hour.csv")#LOAD DATA

#MEMNGURUTKAN DATA
datetime_columns = ["dteday"]
daily_bike_df.sort_values(by="dteday", inplace=True)
daily_bike_df.reset_index(inplace=True)

#MEMASTIKAN KOLOM DATA YANG DIGUNAKAN BERSIFAT `DATETIME`
for column in datetime_columns:
    daily_bike_df[column] = pd.to_datetime(daily_bike_df[column])

#MENGGUNAKAN BATAS TANGGAL AWAL DAN AKHIR
min_date = daily_bike_df["dteday"].min()
max_date = daily_bike_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkvBqi4ukXXttkRI0H6sHPRxMqtzOwFHqW-w&s")
    st.logo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkvBqi4ukXXttkRI0H6sHPRxMqtzOwFHqW-w&s", size="large", icon_image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkvBqi4ukXXttkRI0H6sHPRxMqtzOwFHqW-w&s"
)
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Timeline",min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#start_date dan end_date digunakan untuk memfilter all_df. Data yang telah difilter ini selanjutnya akan disimpan dalam main_df.
main_df = daily_bike_df[(daily_bike_df["dteday"] >= str(start_date)) & 
                (daily_bike_df["dteday"] <= str(end_date))]

#MEMANGGIL HELPER FUNCTION
daily_users_df = create_daily_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)
weatherly_users_df = create_weatherly_users_df(main_df)
weekly_users_df = create_weekly_users_df(main_df)
atmosfer_df = create_atmosfer_df(main_df)
rentday_users_df = create_rentday_users_df(main_df)
monthly_users_df = create_monthly_users_df(main_df)
workholiday_users_df = create_workholiday_users_df(main_df)

#TITLE
st.title("Bike Sharing Rental Dashboard :bike:")

#GRAFIK DAILY ORDER
st.subheader("Daily Users")

col1, col2, col3 = st.columns(3)
 
with col1:
    total_users = daily_bike_df.cnt.sum()
    st.metric("Total Users", value=f"{total_users:,} \U0001F464")
 
with col2:
    total_casual_users = daily_bike_df.casual.sum()
    st.metric("Total Casual Users", value=f"{total_casual_users:,} \U0001F464")

with col3:
    total_registered_users = daily_bike_df.registered.sum()
    st.metric("Total Registered Users", value=f"{total_registered_users:,} \U0001F464")

#GRAFIK NUMBER OF USERS BY DATE
st.subheader("Bike Users by Date")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_users_df["dteday"],
    daily_users_df["Total Users"],
    marker='o', 
    linewidth=2,
    color="#9966CC"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


col1, col2 = st.columns(2)
 
with col1:
    st.subheader("Top 5 Peak Hour Average Bike Users ") #GRAFIK TOP 5 PEAK HOUR OF BIKE USERS BY DAY
    hourly_users_df = hourly_bike_df.groupby(by="hr").agg({
        "cnt" : "mean"
    }).round(0).sort_values(by="cnt", ascending=False).head(5)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = ["#BC8AC2" ]
    hourly_users_df.columns = ["Total Users"]
    hourly_users_df.plot(kind='bar', ax=ax, color=colors)
    ax.set_title("Top 5 Peak Hour of Average Bike Users")
    ax.set_xlabel("Hours")
    ax.set_ylabel("Users")
    ax.tick_params(axis='x', rotation=0)
    plt.tight_layout()
    st.pyplot(fig)

 
with col2:
    bins = [0, 6, 12, 18, 24]
    labels = ["Night", "Morning", "Afternoon", "Evening"]
    hourly_bike_df["Periode"] = pd.cut(hourly_bike_df["hr"], bins=bins, labels=labels, include_lowest=True)
    periode_users_df = hourly_bike_df.groupby(by="Periode").agg({
        "casual" : "mean",
        "registered" : "mean"
    }).round(0).sort_values(by="registered", ascending=False)
    
    st.subheader("Average Bike Users by Periode") #GRAFIK PERIODE
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = ["#9966CC", "#7A378B" ]
    periode_users_df.columns = ["Casual Users", "Registered Users"]
    periode_users_df.plot(kind='bar', ax=ax, stacked=True, color=colors)
    ax.set_title("Average Bike Users by Periode")
    ax.set_xlabel("Periode")
    ax.set_ylabel("Users")
    ax.tick_params(axis='x', rotation=0)
    plt.tight_layout()
    st.pyplot(fig)


#GRAFIK BATANG NUMBER OF USERS BY DAY TYPE
st.subheader("Average Bike Users by Day Type")

fig, ax = plt.subplots(figsize=(8, 3))
workholiday_users_df.columns = ["Casual Users", "Registered Users"]
colors = ["#9966CC", "#7A378B" ]
workholiday_users_df.plot(kind='bar', stacked=True, ax=ax, color=colors)

ax.set_title("Average Bike Users by Day Type")
ax.set_xlabel("Day Type", fontsize=9)
ax.set_ylabel("Users", fontsize=9)
ax.tick_params(axis='x', rotation=0, labelsize=9)
ax.tick_params(axis='y', labelsize=9)  # Rotate x-axis labels
ax.legend(loc="upper right", bbox_to_anchor=(1.4, 1))
plt.tight_layout()
st.pyplot(fig)

#GRAFIK NUMBER OF USERS BY DAY
st.subheader("Average Bike Users by Day")

fig, ax = plt.subplots(figsize=(10, 4))
rentday_users_df.columns = ["Casual Users", "Registered Users"]
colors = ["#9966CC", "#7A378B" ]
rentday_users_df.plot(kind='bar', stacked=True, ax=ax, color=colors)
ax.set_title("Average Bike Users by Day")
ax.set_xlabel("Day")
ax.set_ylabel("Users")
ax.tick_params(axis='x', rotation=0)  # Rotate x-axis labels
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1))
plt.tight_layout()
st.pyplot(fig)


#GRAFIK BATANG MONTHLY BIKE USERS
st.subheader("Monthly Bike Users")

fig, ax = plt.subplots(figsize=(12, 5))
monthly_users_df.columns = ["Casual Users", "Registered Users"]
colors = ["#9966CC", "#7A378B" ]
monthly_users_df.plot(kind='bar', stacked=True, ax=ax, color=colors)
ax.set_title("Monthly Bike Users")
ax.set_xlabel("Month")
ax.set_ylabel("Users")
ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels
ax.legend(loc="upper right", bbox_to_anchor=(1.22, 1))
plt.tight_layout()
st.pyplot(fig)

#GRAFIK BATANG NUMBER OF USERS BY WEATHER
st.subheader("Average Bike Users by Weather")

fig, ax = plt.subplots(figsize=(8, 6))  # Membuat figure dan axes
weatherly_users_df.columns = ["Casual Users", "Registered Users"]
colors = ["#9966CC","#7A378B"]
weatherly_users_df.plot(kind='barh', stacked=True, ax=ax, color=colors)  
ax.set_title("Bike Users by Weather")
ax.set_xlabel("Users")
ax.set_ylabel("Weather")
ax.tick_params(axis='x', rotation=0)  # Agar label x-axis tegak lurus
st.pyplot(fig)

#GRAFIK BATANG NUMBER OF USERS BY SEASON
st.subheader("Average Bike Users by Season")

fig, ax = plt.subplots(figsize=(8, 4))
seasonly_users_df.columns = ["Casual Users", "Registered Users"]
colors = ["#9966CC", "#7A378B" ]
seasonly_users_df.plot(kind='bar', stacked=True, ax=ax, color=colors)
ax.set_title("Bike Users by Season")
ax.set_xlabel("Season", fontsize=12)
ax.set_ylabel("Users", fontsize=12)
ax.tick_params(axis='x', rotation=0, labelsize=12)
ax.tick_params(axis='y', labelsize=12)  # Rotate x-axis labels
ax.legend(loc="upper right", bbox_to_anchor=(1.4, 1))
plt.tight_layout()
st.pyplot(fig)


#KORELASI 
st.subheader("Atmosfer Variable Correlation with Total Bike Users")

correlation_df = atmosfer_df.corr() 
fig, ax = plt.subplots(figsize=(4,3))
sns.heatmap(correlation_df, annot=True, cmap='BuPu', ax=ax)
plt.title("Atmosfer Variable Correlation with Total Bike Users")
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """hum (Humidity), temp (Temperature), windspeed (Windspeed), cnt (Total Users)
        """
    )

st.caption('Copyright (c) Euis Rahmah - Dicoding 2024')
