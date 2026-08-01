import os
import sys
import mlflow

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact

from networksecurity.utils.main_utils.utils import load_object, save_object, load_numpy_array_data ,evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier

import dagshub
dagshub.init(repo_owner='Sho-jin', repo_name='networksecurity', mlflow=True)

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):

        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def track_mlflow(self, model, metrics):
        try:
            with mlflow.start_run():
                f1_score = metrics.f1_score
                precision = metrics.precision_score
                recall = metrics.recall_score

                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision", precision)
                mlflow.log_metric("recall", recall)

                mlflow.sklearn.log_model(model, "model")

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def train_model(self, x_train, y_train,x_test, y_test):
        try:
           models = {
               "LogisticRegression": LogisticRegression(verbose=1),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "KNeighborsClassifier": KNeighborsClassifier(),
                "RandomForestClassifier": RandomForestClassifier(verbose=1),
                "GradientBoostingClassifier": GradientBoostingClassifier(verbose=1),
                "AdaBoostClassifier": AdaBoostClassifier()

           }

           params = {
                "LogisticRegression": {},
                "DecisionTreeClassifier": {
                        "criterion": ["gini", "entropy"],
                        "max_depth": [5, 10, 15]
                },
                "KNeighborsClassifier": {
                     'n_neighbors': [3, 5, 7],
                     'weights': ['uniform', 'distance']
                },
                "RandomForestClassifier": {
                     'n_estimators': [8,16, 32,64,128,256]
                     
                },
                "GradientBoostingClassifier": {
                     'learning_rate': [0.01, 0.1,0.05,0.001],
                     'subsample': [0.5, 0.7, 1.0]
                     
                },
                "AdaBoostClassifier": {
                     'n_estimators': [8,16, 32,64,128,256],
                     'learning_rate': [0.01, 0.1,0.05,0.001]
                }
              }
           
           model_report:dict = evaluate_models(x_train,y_train,x_test,y_test,models,params)

           best_model_score = max(sorted(model_report.values()))

           best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

           best_model = models[best_model_name]

           best_model.fit(x_train, y_train)

           y_train_pred = best_model.predict(x_train)

           classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

           #ML FLOW
           self.track_mlflow(model=best_model, metrics=classification_train_metric)

           y_test_pred = best_model.predict(x_test)

           classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

           self.track_mlflow(model=best_model, metrics=classification_test_metric)

           preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

           model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
           os.makedirs(model_dir_path, exist_ok=True)

           network_model = NetworkModel(preprocessor=preprocessor, model=best_model)

           save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model)

           save_object("final_models/model.pkl", best_model)

           model_trainer_artifact = ModelTrainerArtifact( 
               
               trained_model_file_path=self.model_trainer_config.trained_model_file_path,
               train_metric_path=classification_train_metric,
                test_metric_path=classification_test_metric
           )

           logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
           return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            model_trainer_artifact = self.train_model(
            x_train,
            y_train,
            x_test,
            y_test
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)  