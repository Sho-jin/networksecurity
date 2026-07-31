import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_DB_URL")

print(f"MongoDB URL: {MONGO_URL}")


ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_URL)
            self.db = self.client["NetworkSecurity"]
            self.collection = self.db["network_data"]
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def cv_to_json_convertor(self, file_path: str):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records  
            self.mongo_client = pymongo.MongoClient(MONGO_URL)

            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

if __name__ == "__main__":
    file_path = "Network_Data/phisingData.csv"
    collection_name = "network_data"
    database_name = "NetworkSecurity"
    networkobj = NetworkDataExtract()
    records = networkobj.cv_to_json_convertor(file_path)
    no_of_records = networkobj.insert_data_to_mongodb(records, database_name, collection_name)
    print(f"Inserted {no_of_records} records into the MongoDB collection '{collection_name}' in database '{database_name}'.")

