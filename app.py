import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Set Streamlit page configuration (wide layout)
st.set_page_config(layout="wide")

# MongoDB Atlas Connection (Replace with your own credentials)
MONGO_URI = "mongodb+srv://admin:admin123@data.ywf1x.mongodb.net/?retryWrites=true&w=majority&appName=data"
client = MongoClient(MONGO_URI)
db = client["stock_database"]
collection = db["stock_data"]

# Streamlit App Title
st.title("Stock Data Explorer")

# Fetch All Data from MongoDB
@st.cache_data
def get_full_data():
    data = list(collection.find())  # Fetch all data
    return data

# Fetch Limited Data (200 entries for initial display)
@st.cache_data
def get_limited_data():
    data = list(collection.find().limit(200))  # Limit data to 200 entries
    return data

# Highlight Columns
highlight_columns = ["%_of_curr", "3m_%", "6m_%", "9m_%", "12m_%"]

# Highlight percentages
def highlight_percentages(val):
    if pd.isnull(val):
        return ""
    try:
        val = float(str(val).replace("%", ""))  # Remove '%' and convert to float
        return "color: green;" if val > 0 else "color: red;" if val < 0 else ""
    except ValueError:
        return ""

# Style DataFrame
def style_dataframe(df):
    df = df.copy()
    for col in highlight_columns:
        if col in df.columns:
            df[col] = df[col].astype(str)  # Ensure all values are strings for consistency
    return df.style.applymap(highlight_percentages, subset=highlight_columns)\
                   .apply(lambda x: ['background-color: #f9f9f9' if i % 2 == 0 else '' for i in range(len(x))], axis=0)

# Fetch data
full_data = get_full_data()
limited_data = get_limited_data()

if full_data:
    full_df = pd.DataFrame(full_data).drop("_id", axis=1)
    full_df["date"] = pd.to_datetime(full_df["date"], format="%d-%m-%Y").dt.date.astype(str)  # Correct date format

if limited_data:
    limited_df = pd.DataFrame(limited_data).drop("_id", axis=1)
    limited_df["date"] = pd.to_datetime(limited_df["date"], format="%d-%m-%Y").dt.date.astype(str)  # Correct date format

    
   # Sidebar Filters
    st.sidebar.header("Filters")

    # Year Filter (Standalone)
    year_filter = st.sidebar.selectbox("Select Year", [""] + sorted(full_df["date"].apply(lambda x: x[:4]).unique()), key="year")

    # Month and Day Filters Side-by-Side
    col1, col2 = st.sidebar.columns(2)

    # Select Month
    month_filter = ""
    if year_filter:
        months = sorted(full_df[full_df["date"].str.startswith(year_filter)]["date"].apply(lambda x: x[5:7]).unique())
        month_filter = col1.selectbox("Select Month", [""] + months, key="month")

    # Select Day
    day_filter = ""
    if month_filter:
        days = sorted(full_df[(full_df["date"].str.startswith(f"{year_filter}-{month_filter}"))]["date"].apply(lambda x: x[8:10]).unique())
        day_filter = col2.selectbox("Select Day", [""] + days, key="day")

    # Client Name Filter (Standalone)
    client_name_filter = st.sidebar.selectbox("Client Name", [""] + sorted(full_df["client_name"].unique()), key="client")

    # Security Name Filter (Standalone)
    security_name_filter = st.sidebar.selectbox("Security Name", [""] + sorted(full_df["security_name"].unique()), key="security")

    # Buy/Sell and Type Filters Side-by-Side
    col3, col4 = st.sidebar.columns(2)

    # Buy/Sell Filter
    buy_sell_filter = col3.selectbox("Buy/Sell", [""] + sorted(full_df["buy_sell"].unique()), key="buy_sell")

    # Type Filter
    type_filter = col4.selectbox("Type", [""] + sorted(full_df["type"].unique()), key="type")

    # Add margin (empty space) between filters and buttons
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    # Apply and Clear Filters buttons
    col5, col6 = st.sidebar.columns(2)
    apply_button = col5.button("Apply Filters")
    clear_button = col6.button("Clear Filters")




    if clear_button:
        apply_button = False  # Reset filters

    # Display limited data initially
    if not apply_button:
        st.write("Showing initial 200 entries (use filters to refine results):")
        st.dataframe(style_dataframe(limited_df))
    else:
        # Apply filters on the full dataset
        filtered_data = full_df

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

        # Apply buy/sell filter if selected
        if buy_sell_filter:
            filtered_data = filtered_data[filtered_data["buy_sell"] == buy_sell_filter]

        # Apply type filter if selected
        if type_filter:
            filtered_data = filtered_data[filtered_data["type"] == type_filter]

        # Display filtered data
        if not filtered_data.empty:
            st.write(f"Showing {len(filtered_data)} filtered results:")
            st.dataframe(style_dataframe(filtered_data))
        else:
            st.write("No data found for the selected filters.")
else:
    st.write("No data found.")
