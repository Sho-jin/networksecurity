import os
import sys
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import pandas as pd
import numpy as np
import pymongo
from sklearn.model_selection import train_test_split
from typing import List

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df = df.drop(columns=["_id"],axis=1)

            df.replace(to_replace="na",value=np.NAN,inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_to_feature_store(self,df:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            df.to_csv(feature_store_file_path,index=False,header=True)
            return df
    
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self, df:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed Train Test Split")

            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting training and test data")

            train_set.to_csv(self.data_ingestion_config.train_file_path, index = False, header = True)

            test_set.to_csv(self.data_ingestion_config.test_file_path, index = False, header = True)

            logging.info("Exported training and test data")
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            data = self.export_collection_as_dataframe()
            data = self.export_data_to_feature_store(data)
            self.split_data_as_train_test(data)

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path = self.data_ingestion_config.train_file_path,
                test_file_path = self.data_ingestion_config.test_file_path
                )
            
            return data_ingestion_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)