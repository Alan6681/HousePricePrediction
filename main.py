from housepriceprediction.components.data_ingestion import DataIngestion
from housepriceprediction.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from housepriceprediction.logging.logger import logging
from housepriceprediction.exception.exception import HousePricePredictionException
import sys

def data_ingestion_training_pipeline():
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config)

    artifact = data_ingestion.initiate_ingestion()

    
    print("Feature Store Path:", artifact.feature_store_file_path)
    print("Train File Path:", artifact.train_file_path)
    print("Test File Path:", artifact.test_file_path)
    print("SUCCESS: Data ingestion completed!")

if __name__ == "__main__":
    data_ingestion_training_pipeline()
    
    