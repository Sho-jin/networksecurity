import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.constant.training_pipeline import MODEL_FILE_NAME, SAVED_MODEL_DIR

class NetworkModel:
    def __init__(self, model, preprocessor):
        try:
            self.model = model
            self.preprocessor = preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, X):
        try:
            X_transformed = self.preprocessor.transform(X)
            y_pred = self.model.predict(X_transformed)
            return y_pred
        except Exception as e:
            raise NetworkSecurityException(e, sys)
