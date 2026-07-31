from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig,trainingPipelineConfig,DataValidationConfig

from networksecurity.components.data_validation import DataValidation

import sys

if __name__ =="__main__":
    try:
        training_pipeline_config = trainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)

        logging.info("Initiate the data Ingestion")

        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        print(data_ingestion_artifact)

        logging.info("Initiate the dData Validation")

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        data_ingestion_artifact = data_validation.initiate_data_validation()



    except Exception as e:
        raise NetworkSecurityException(e,sys)
