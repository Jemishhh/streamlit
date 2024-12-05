from pymongo import MongoClient

# MongoDB Connection (Replace with your own URI)
MONGO_URI = "mongodb+srv://admin:admin123@data.ywf1x.mongodb.net/?retryWrites=true&w=majority&appName=data"
client = MongoClient(MONGO_URI)
db = client["stock_database"]
collection = db["stock_data"]

# Delete all documents in the collection
collection.delete_many({})  # Empty filter to delete all documents

print("All documents deleted.")
