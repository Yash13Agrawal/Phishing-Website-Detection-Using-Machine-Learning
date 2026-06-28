import os
import sys
from dotenv import load_dotenv
from database_connect import mongo_operation as mongo

# Load environment variables from .env
load_dotenv()

def upload_data():
    mongo_url = os.getenv("MONGO_DB_URL")
    
    if not mongo_url or "<username>" in mongo_url or "cluster0.mongodb.net" in mongo_url and "<password>" in mongo_url:
        print("ERROR: Please configure your MONGO_DB_URL in the .env file with your actual MongoDB credentials.")
        print("Example: MONGO_DB_URL=\"mongodb+srv://your_username:your_password@your_cluster.mongodb.net/?retryWrites=true&w=majority\"")
        sys.exit(1)
        
    database_name = "phising"
    csv_filename = "phising_08012020_120000.csv"
    collection_name = "phising_08012020_120000"
    
    # Path to the CSV file
    csv_file_path = os.path.join("upload_data_to_db", csv_filename)
    
    if not os.path.exists(csv_file_path):
        print(f"ERROR: Could not find the CSV file at {csv_file_path}")
        sys.exit(1)
        
    print(f"Uploading {csv_file_path} to MongoDB Database: '{database_name}', Collection: '{collection_name}'...")
    
    try:
        mongo_connection = mongo(
            client_url=mongo_url,
            database_name=database_name,
            collection_name=collection_name
        )
        mongo_connection.bulk_insert(csv_file_path)
        print("SUCCESS: Data uploaded successfully to MongoDB!")
    except Exception as e:
        print(f"ERROR: Failed to upload data. Details:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    upload_data()
