import os
import sys
import numpy as np
import pandas as pd

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_INPUT_PARAMS, TARTGET_COLUMN
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformer_object(self) -> Pipeline:
        try:
            IMPUTER  = KNNImputer(**DATA_TRANSFORMATION_INPUT_PARAMS)
            processor:Pipeline = Pipeline([("Imputer",IMPUTER)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)

            target_column_name = TARTGET_COLUMN

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            processor = self.get_data_transformer_object()

            processor_object = processor.fit(input_feature_train_df)
            transformed_input_train_feature = processor_object.transform(input_feature_train_df)
            transformed_input_test_feature = processor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,processor_object)

            save_object("final_models/preprocessor.pkl",processor_object)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)

        