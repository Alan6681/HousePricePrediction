import os
from datetime import datetime

from housepriceprediction.constants.file_paths import ARTIFACTS_DIR

from housepriceprediction.constants.file_paths import (
RAW_DATA_DIR, RAW_TRAIN_FILE_PATH, RAW_TEST_FILE_PATH,
DATA_INGESTION_DIR, DATA_INGESTION_FEATURE_STORE, DATA_INGESTION_INGESTED_DIR,
TRAIN_FILE_PATH, TEST_FILE_PATH)

class TrainingPipelineConfig:
    def __init__(self):
        timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = "HousePricePrediction"
        self.artifact_dir = os.path.join(ARTIFACTS_DIR, timestamp)
        self.timestamp = timestamp

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Raw Data Paths
        self.raw_data_dir: str = RAW_DATA_DIR
        self.raw_train_file_path: str = RAW_TRAIN_FILE_PATH
        self.raw_test_file_path: str = RAW_TEST_FILE_PATH

        # Main data ingestion directory
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR)

        # Feature store directory
        self.feature_store_dir: str = os.path.join(self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE)

        # Ingested data directory
        self.ingested_dir: str = os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR)

        # Output train and test file paths for ingested data
        self.ingested_train_file_path: str =os.path.join(self.ingested_dir, TRAIN_FILE_PATH)
        self.ingested_test_file_path: str = os.path.join(self.ingested_dir, TEST_FILE_PATH)
    