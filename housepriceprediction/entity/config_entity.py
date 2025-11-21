import os
from datetime import datetime

from housepriceprediction.constants.file_paths import ARTIFACTS_DIR, SCHEMA_DIR

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
        # self.raw_test_file_path: str = RAW_TEST_FILE_PATH

        # Main data ingestion directory
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR)

        # Feature store directory
        self.feature_store_dir: str = os.path.join(self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE)

        # Ingested data directory
        self.ingested_dir: str = os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR)

        # Output train and test file paths for ingested data
        self.ingested_train_file_path: str =os.path.join(self.ingested_dir, TRAIN_FILE_PATH)
        self.ingested_test_file_path: str = os.path.join(self.ingested_dir, TEST_FILE_PATH)

        # Schema file path
        

class DataValidationConfig:
    def __init__(self, data_ingestion_config: DataIngestionConfig):

    #TODO: 1. Set the data_validation dir path
    # 2. Set the validated data dir path
    # 3. Set the Invalid data dir path
    # 4. Set the drift_report yaml file dir path
    # 5. Set the schema file path
    # 6. Set or collect the train and test file part from the DataIngestionArtifact

        # 1. Set the data_validation dir path
        self.validation_dir = os.path.join(data_ingestion_config.data_ingestion_dir, "data_validation")

        # 2. Set validated data dir path for train and test
        self.valid_train_path = os.path.join(self.validation_dir, "valid_train.csv")
        self.valid_test_path = os.path.join(self.validation_dir, "valid_test.csv")

        # 3. Set invalid data dir path
        self.invalid_train_path = os.path.join(self.validation_dir, "invalid_train.csv")
        self.invalid_test_path = os.path.join(self.validation_dir, "invalid_test.csv")

        # 4. Set the drift_report yaml file dir path
        self.drift_report_file_path = os.path.join(self.validation_dir, "drift_report.yaml")

        # 5. Set the schema file path 
        self.schema_file_path = os.path.join(SCHEMA_DIR, "schema.yaml")

        # 6. Collect the train and test file part from the DataIngestionArtifact
        self.train_file_path = data_ingestion_config.ingested_train_file_path
        self.test_file_path = data_ingestion_config.ingested_test_file_path