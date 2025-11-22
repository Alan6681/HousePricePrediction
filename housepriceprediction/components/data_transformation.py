from housepriceprediction.exception.exception import HousePricePredictionException
from housepriceprediction.logging.logger import logging
from housepriceprediction.constants.training_pipeline.constants import *
from housepriceprediction.constants.file_paths import *
from housepriceprediction.entity.config_entity import DataTransformationConfig, DataValidationConfig
from housepriceprediction.utils.main_utils.utils import read_yaml_file, save_numpy_array_data, save_object
from housepriceprediction.entity.artifacts_entity import DataValidationArtifact, DataTransformationArtifact

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OneHotEncoder

import numpy as np
import pandas as pd
import os
import sys


class DataTransformation:
    def __init__(self, data_validation_config: DataValidationConfig, 
                 data_validation_artifact: DataValidationArtifact, 
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_config = data_validation_config
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self.schema_config = read_yaml_file(self.data_validation_config.schema_file_path)
        except Exception as e:
            raise HousePricePredictionException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise HousePricePredictionException(e, sys)

    def get_column_type(self, col_type: str):
        try:
            if col_type == "categorical":
                return list(self.schema_config["categorical"])
            elif col_type == "numerical":
                return list(self.schema_config["numerical"])
            else:
                raise ValueError("col_type must be 'categorical' or 'numerical'")
        except Exception as e:
            raise HousePricePredictionException(e, sys)

    def get_data_transformed_object(self, input_df: pd.DataFrame) -> ColumnTransformer:
        """Creates a ColumnTransformer safely using only existing columns"""
        try:
            logging.info("Creating data transformation object (ColumnTransformer)")

            numerical_columns = [col for col in self.get_column_type("numerical") if col in input_df.columns]
            categorical_columns = [col for col in self.get_column_type("categorical") if col in input_df.columns]

            logging.info(f"Numerical columns: {numerical_columns}")
            logging.info(f"Categorical columns: {categorical_columns}")

            num_pipeline = Pipeline([
                ('imputer', KNNImputer(**DATA_TRANSFORMED_IMPUTER_PARAMS))
            ])

            cat_pipeline = Pipeline([
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ])

            preprocessor = ColumnTransformer(
                transformers=[
                    ('numerical', num_pipeline, numerical_columns),
                    ('categorical', cat_pipeline, categorical_columns)
                ],
                remainder='drop'  # drop any columns not specified in schema
            )

            logging.info("ColumnTransformer created successfully")
            return preprocessor

        except Exception as e:
            raise HousePricePredictionException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation process")

            # Read validated train and test datasets
            train_df = self.read_data(self.data_validation_artifact.valid_train_df)
            test_df = self.read_data(self.data_validation_artifact.valid_test_df)
            logging.info(f"Train shape: {train_df.shape}, Test shape: {test_df.shape}")

            # Split features and target
            input_feature_train_df = train_df.drop(columns=TARGET_COLUMN, axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=TARGET_COLUMN, axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Create ColumnTransformer
            preprocessor = self.get_data_transformed_object(input_feature_train_df)

            # Apply transformations
            transformed_train_input_feature = preprocessor.fit_transform(input_feature_train_df)
            transformed_test_input_feature = preprocessor.transform(input_feature_test_df)

            logging.info(f"Transformed train shape: {transformed_train_input_feature.shape}")
            logging.info(f"Transformed test shape: {transformed_test_input_feature.shape}")

            # Ensure target arrays are 2D for concatenation
            target_train_array = np.array(target_feature_train_df).reshape(-1, 1)
            target_test_array = np.array(target_feature_test_df).reshape(-1, 1)

            # Combine features and target
            train_arr = np.c_[transformed_train_input_feature, target_train_array]
            test_arr = np.c_[transformed_test_input_feature, target_test_array]

            logging.info("Combined features and target into final arrays")

            # Save transformed arrays and preprocessor object
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor)
            save_object("final_models/preprocessor.pkl", preprocessor)

            logging.info("Saved transformed arrays and preprocessor object successfully")

            return DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                preprocessed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )

        except Exception as e:
            raise HousePricePredictionException(e, sys)
