from housepriceprediction.exception.exception import HousePricePredictionException
from housepriceprediction.logging.logger import logging
from housepriceprediction.constants.training_pipeline.constants import *
import sys
import os

class HousePricePredictionModel:
    def __init__(self, preprocessor, model):
        """
        Initialize the HousePricePredictionModel with a preprocessor and a trained model.

        Args:
            preprocessor: The preprocessing object (e.g., ColumnTransformer, Pipeline).
            model: The trained machine learning model.
        """
        self.preprocessor = preprocessor
        self.model = model

    def predict(self, X):
        """
        Make predictions on the input data after applying preprocessing.

        Args:
            X: Input features for prediction.

        Returns:
            Predicted values.
        """
        try:
            X_transformed = self.preprocessor.transform(X)
            predictions = self.model.predict(X_transformed)
            return predictions
        except Exception as e:
            raise HousePricePredictionException(e, sys)