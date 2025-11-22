from housepriceprediction.exception.exception import HousePricePredictionException
from housepriceprediction.logging.logger import logging
from housepriceprediction.entity.artifacts_entity import RegressionMetricArtifact
from sklearn.metrics import root_mean_squared_error, r2_score
import sys
import os

def get_regression_metrics(y_true, y_preds) -> dict:
    try:
        model_rmse_score = root_mean_squared_error(y_true, y_preds)
        model_r2_score = r2_score(y_true, y_preds)

        regression_metric_artifact = RegressionMetricArtifact(
            r2_score=model_r2_score,
            root_mean_squared_error=model_rmse_score
        )

        return regression_metric_artifact
    except Exception as e:
        raise HousePricePredictionException(e, sys)