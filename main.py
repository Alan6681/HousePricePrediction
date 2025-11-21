from housepriceprediction.components.data_ingestion import DataIngestion
from housepriceprediction.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from housepriceprediction.logging.logger import logging
from housepriceprediction.exception.exception import HousePricePredictionException
import sys
import pandas as pd


from housepriceprediction.components.data_validation import DataValidation
from housepriceprediction.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from housepriceprediction.logging.logger import logging



def data_ingestion_training_pipeline():
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)

        artifact = data_ingestion.initiate_ingestion()

        
        print("Feature Store Path:", artifact.feature_store_file_path)
        print("Train File Path:", artifact.train_file_path)
        print("Test File Path:", artifact.test_file_path)
        print("SUCCESS: Data ingestion completed!")
    except Exception as e:
        raise HousePricePredictionException(e, sys)

def data_validation_training_pipeline():
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)

        data_ingestion_artifact = data_ingestion.initiate_ingestion()

        data_validation_config = DataValidationConfig(data_ingestion_config= data_ingestion_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)

        data_validation_artifact = data_validation.initiate_data_validation()

        logging.info("Data Validation completed!")
        print("Valid Train File Path:", data_validation_config.valid_train_path)
        print("Valid Test File Path:", data_validation_config.valid_test_path)
        print("Drift Report File Path:", data_validation_config.drift_report_file_path)

    except Exception as e:
        raise HousePricePredictionException(e, sys)
    
    

if __name__ == "__main__":

    data_ingestion_training_pipeline()
    data_validation_training_pipeline()
    