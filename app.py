import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# Set Streamlit page configuration (wide layout)
st.set_page_config(layout="wide")

# MongoDB Atlas Connection (Replace with your own credentials)
MONGO_URI = "mongodb+srv://admin:admin123@data.ywf1x.mongodb.net/?retryWrites=true&w=majority&appName=data"
client = MongoClient(MONGO_URI)
db = client["stock_database"]
collection = db["stock_data"]

# Streamlit App Title
st.title("Stock Data Explorer")

# Fetch Data from MongoDB (limit to 200 entries for now)
@st.cache_data
def get_data():
    data = list(collection.find().limit(200))  # Limit the data to 200 entries
    return data

# Drop _id field and convert data to DataFrame
data = get_data()
if data:
    df = pd.DataFrame(data).drop("_id", axis=1)

    # Convert 'date' column to datetime format
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d").dt.date.astype(str)

    # Sidebar Filters
    st.sidebar.header("Filters")

    # Select Year
    years = sorted(df["date"].apply(lambda x: x[:4]).unique())
    year_filter = st.sidebar.selectbox("Select Year", [""] + years)

    # Initialize month_filter and day_filter
    month_filter = ""
    day_filter = ""

    if year_filter:
        # Select Month
        months = sorted(df[df["date"].str.startswith(year_filter)]["date"].apply(lambda x: x[5:7]).unique())
        month_filter = st.sidebar.selectbox("Select Month", [""] + months)

    if month_filter:
        # Select Day
        days = sorted(df[(df["date"].str.startswith(f"{year_filter}-{month_filter}"))]["date"].apply(lambda x: x[8:10]).unique())
        day_filter = st.sidebar.selectbox("Select Day", [""] + days)

    # Unique client names for the client name filter
    client_names = sorted(df["client_name"].unique())
    client_name_filter = st.sidebar.selectbox("Client Name", [""] + client_names)

    # Unique security names for the security name filter
    security_names = sorted(df["security_name"].unique())
    security_name_filter = st.sidebar.selectbox("Security Name", [""] + security_names)

    # Unique types for the type filter (cast to string)
    df["type"] = df["type"].astype(str)  # Convert type column to strings
    types = sorted(df["type"].unique())
    type_filter = st.sidebar.selectbox("Type", [""] + types)

    # Apply Filters button
    apply_button = st.sidebar.button("Apply Filters")

    # Initially show all data (without any filter applied)
    if not apply_button:
        st.write("Showing all data (up to 200 entries):")
        st.dataframe(df)
    else:
        # Apply filters only when the Apply Filters button is clicked
        filtered_data = df

        # Apply year filter if selected
        if year_filter:
            filtered_data = filtered_data[filtered_data["date"].str.startswith(year_filter)]

        # Apply month filter if selected
        if month_filter:
            filtered_data = filtered_data[filtered_data["date"].str.startswith(f"{year_filter}-{month_filter}")]

        # Apply day filter if selected
        if day_filter:
            filtered_data = filtered_data[filtered_data["date"].str.startswith(f"{year_filter}-{month_filter}-{day_filter}")]

        # Apply client name filter if selected
        if client_name_filter:
            filtered_data = filtered_data[filtered_data["client_name"] == client_name_filter]

        # Apply security name filter if selected
        if security_name_filter:
            filtered_data = filtered_data[filtered_data["security_name"] == security_name_filter]

        # Apply type filter if selected
        if type_filter:
            filtered_data = filtered_data[filtered_data["type"] == type_filter]

        # Display filtered data
        if not filtered_data.empty:
            st.write(f"Showing {len(filtered_data)} filtered results:")
            st.dataframe(filtered_data)
        else:
            st.write("No data found for the selected filters.")
else:
    st.write("No data found.")
