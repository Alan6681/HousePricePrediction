from housepriceprediction.components.data_ingestion import DataIngestion
from housepriceprediction.entity.config_entity import DataValidationConfig
from housepriceprediction.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from housepriceprediction.exception.exception import HousePricePredictionException
from housepriceprediction.logging.logger import logging
import pandas as pd
from housepriceprediction.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp

import os
import sys

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self.schema_config = read_yaml_file(self.data_validation_config.schema_file_path)

    def read_data(self, file_path:str) -> pd.DataFrame:
        """Reads a CSV file into a pandas DataFrame"""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise HousePricePredictionException(e,sys)
        

    def validate_number_of_columns(self, dataframe:pd.DataFrame) -> bool:
        """Validates if the DataFrame has the expected number of columns"""
        try:
            dataframe_columns = dataframe.shape[1]
            required_columns = len(self.schema_config["schema"]["columns"])

            logging.info(f"Required number of columns: {required_columns}")
            logging.info(f"DataFrame has columns: {dataframe_columns}")

            return dataframe_columns == required_columns
        except Exception as e:
            raise HousePricePredictionException(e,sys)
        
    def required_columns(self, dataframe:pd.DataFrame) -> bool:
        """Validates if the DataFrame contains all required columns"""
        try:
            required_columns = list(self.schema_config["schema"]["columns"].keys())
            dataframe_columns = dataframe.columns
            missing_columns = [col for col in required_columns if col not in dataframe_columns]

            if missing_columns:
                logging.info(f"Missing columns in: {missing_columns}")
                return False
            return True
            
        except Exception as e:
            raise HousePricePredictionException(e,sys)
        
    def detect_data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, threshold=0.05) -> bool:
        """Checks for Datadrift between training set and test sets"""
        try:
            check = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                test_result = ks_2samp(d1, d2)
                p_value = float(test_result.pvalue)
                drift_found = p_value < threshold

                report[column] = {
                    "p_value" : p_value,
                    "drift_found" : drift_found
                }

                if drift_found:
                    check = False


            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path, content=report)
            return check
        except Exception as e:
            raise HousePricePredictionException(e, sys)
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        """Main pipeline entry: validate schema, columns, and drift."""
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = self.read_data(train_file_path)
            test_df = self.read_data(test_file_path)

            # Validate number of columns
            if not self.validate_number_of_columns(train_df):
                raise Exception("The number of columns in train_df does not match training data")
            if not self.validate_number_of_columns(test_df):
                raise Exception("The number of columns in test_df does not match test data")


            # Validate required columns
            if not self.required_columns(train_df):
                raise Exception ("Required columns are missing in train_df")
            if not self.required_columns(test_df):
                raise Exception ("Required columns are missing in test_df")
            
            # Detect DataDrift
            validation_status = self.detect_data_drift(base_df=train_df, current_df=test_df)
            if not validation_status:
                logging.info("Data drift detected between train and test datasets")
            

            # Save valid datasets
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_path), exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_path, index=False)
            test_df.to_csv(self.data_validation_config.valid_test_path, index=False)


            # Prepare Artifact
            data_validation_artifact = DataValidationArtifact(
                
                valid_train_df= self.data_validation_config.valid_train_path,
                valid_test_df= self.data_validation_config.valid_test_path,
                invalid_train_df= self.data_validation_config.invalid_train_path,
                invalid_test_df= self.data_validation_config.invalid_test_path,
                drift_report_file_path= self.data_validation_config.drift_report_file_path,
                validation_status=validation_status
                

            )

            logging.info(f"Data Validation Completed Successfully {data_validation_artifact}")
            return data_validation_artifact


        except Exception as e:
            raise HousePricePredictionException(e, sys)


    


    
