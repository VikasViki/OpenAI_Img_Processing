import pandas as pd
from pymongo import MongoClient, ASCENDING

# Step 1: Load CSV data
csv_file = "img.csv"
data = pd.read_csv(csv_file)

# Step 2: Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["img_database"]  
collection = db["img_collection"]

# Step 3: Insert data into MongoDB
# Convert the DataFrame to a list of dictionaries
data_dict = data.to_dict(orient="records")

# Insert data into the collection
collection.insert_many(data_dict)
collection.create_index([("depth", ASCENDING)])

print("Data has been successfully loaded into MongoDB and 'depth' is column is Indexed! ")