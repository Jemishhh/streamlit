import pandas as pd
from pymongo import MongoClient

# Replace with your MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://admin:admin123@data.ywf1x.mongodb.net/?retryWrites=true&w=majority&appName=data"
client = MongoClient(MONGO_URI)

# Access Database and Collection
db = client["stock_database"]  # Replace with your database name
collection = db["stock_data"]  # Replace with your collection name

# Load CSV Data
file_path = "C:\\Users\\jemis\\temp\\Streamlit\\fine_percent.csv"  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Ensure proper column names for MongoDB
df.columns = df.columns.str.strip().str.replace(' ', '_')  # Replace spaces with underscores
df.columns = df.columns.str.lower()  # Convert column names to lowercase for consistency

# Insert Data
try:
    collection.insert_many(df.to_dict("records"))
    print(f"Inserted {len(df)} records into MongoDB, including new columns!")
except Exception as e:
    print(f"Error inserting data: {e}")
