import pandas as pd
from pymongo import MongoClient

# Replace with your MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://admin:admin123@data.ywf1x.mongodb.net/?retryWrites=true&w=majority&appName=data"
client = MongoClient(MONGO_URI)

# Access Database and Collection
db = client["stock_database"]  # Replace with your database name
collection = db["stock_data"]  # Replace with your collection name

# Load CSV Data
df = pd.read_csv("C:\\Users\\jemis\\temp\\Streamlit\\test_mongo.csv")

# Insert Data
try:
    collection.insert_many(df.to_dict("records"))
    print(f"Inserted {len(df)} records into MongoDB!")
except Exception as e:
    print(f"Error inserting data: {e}")
