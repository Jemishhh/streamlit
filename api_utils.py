from pymongo import MongoClient

# MongoDB Atlas Connection (Replace with your own credentials)
MONGO_URI = "mongodb+srv://admin:admin123@data.ywf1x.mongodb.net/?retryWrites=true&w=majority&appName=data"
client = MongoClient(MONGO_URI)
db = client["stock_database"]
collection = db["stock_data"]

# Update the 'type' field to strip any leading/trailing spaces
collection.update_many(
    {"type": {"$exists": True}},  # Ensure 'type' field exists
    [
        {"$set": {"type": {"$trim": {"input": "$type"}}}}  # Trim whitespace from 'type' field
    ]
)

print("Whitespace removed from 'type' field in all documents.")
