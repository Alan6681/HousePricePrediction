from housepriceprediction.exception.exception import HousePricePredictionException
from housepriceprediction.logging.logger import logging
from housepriceprediction.entity.config_entity import ModelTrainerConfig
from housepriceprediction.entity.artifacts_entity import DataTransformationArtifact, ModelTrainerArtifact
from housepriceprediction.utils.ml_utils.metrics.Regression_metrics import get_regression_metrics
from housepriceprediction.utils.main_utils.utils import load_numpy_array, load_object, save_object, evaluate_models
from housepriceprediction.entity.config_entity import DataTransformationConfig
from housepriceprediction.utils.ml_utils.model.estimator import HousePricePredictionModel
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
import sys
import os
import mlflow

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise HousePricePredictionException(e,sys)

    def track_mlflow(self, best_model, regressionmetric):
        with mlflow.start_run():
            rmse_score = regressionmetric.rmse_score
            r2_score = regressionmetric.r2_score

            mlflow.log_metric("rmse_score", rmse_score)
            mlflow.log_metric("r2_score", r2_score)
            mlflow.sklearn.log_model(best_model, "model")


    def train_model(self, X_train, y_train, X_test, y_test):
        model = {
            "LinearRegression": LinearRegression(),
            "DecisionTreeRegressor": DecisionTreeRegressor(),
            "RandomForestRegressor": RandomForestRegressor(verbose=1),
            
            
        }

        params = {

            "LinearRegression": {
                "fit_intercept": [True, False],
            },
            "DecisionTreeRegressor": {
                "max_depth": [None, 5, 10],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
                "max_features": ["auto", "sqrt"],
                "criterion": ["squared_error", "friedman_mse", "absolute_error"]
            },
            "RandomForestRegressor": {
                "n_estimators": [100, 200, 300],
                "max_depth": [None, 20, 30],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
                "max_features": ["auto", "sqrt"],
            }
        }

        model_report: dict = evaluate_models( X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=model, param=params)
        
        # Get the best model score from the report
        best_model_score = max(sorted(model_report.values()))

        # Get the best model name from the report
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model = model[best_model_name]
        y_train_pred = best_model.predict(X_train)

        regression_train_metric = get_regression_metrics(y_true=y_train, y_preds=y_train_pred)
        # logging.info(f"Best found model on both training and testing dataset is {best_model_name} with r2_score: {best_model_score}")

        # Track the mlflow
        self.track_mlflow(best_model, regression_train_metric)

        y_test_pred = best_model.predict(X_test)
        regression_test_metric = get_regression_metrics(y_true=y_test, y_preds=y_test_pred)

        #Track mlflow
        self.track_mlflow(best_model, regression_test_metric)

        preprocessor = load_object(self.data_transformation_artifact.preprocessed_object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.model_trained_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        houseprice_prediction_model = HousePricePredictionModel(preprocessor=preprocessor, model=best_model)

        save_object(self.model_trainer_config.model_trained_file_path, houseprice_prediction_model)
        save_object("final_models/best_model.pkl", best_model)

        is_model_accepted = best_model_score >= self.model_trainer_config.model_trainer_expected_r2_score
        print(f"The best model_score is: {best_model_score}")
        print(f"The regression_test_metric is  {regression_test_metric} ")


        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.model_trained_file_path,
            train_metric_artifact=regression_train_metric,
            test_metric_artifact= regression_test_metric,
            is_model_accepted=is_model_accepted
            )

        logging.info(f"Model trianer artifact: {model_trainer_artifact}")
        return model_trainer_artifact
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # Loading Training arr and Testing arr
            train_arr = load_numpy_array(train_file_path)
            test_arr = load_numpy_array(test_file_path)

            X_train,y_train,X_test,y_test = (
                    train_arr[:, :-1],
                    train_arr[:, -1],
                    test_arr[:, :-1],
                    test_arr[:, -1]
                )
            
            model_trainer_artifact = self.train_model(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)

            return model_trainer_artifact


        except Exception as e:
            raise HousePricePredictionException(e,sys)



