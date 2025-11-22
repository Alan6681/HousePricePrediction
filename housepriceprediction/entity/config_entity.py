import os
from datetime import datetime

from housepriceprediction.constants.file_paths import ARTIFACTS_DIR, SCHEMA_DIR

from housepriceprediction.constants import file_paths



class TrainingPipelineConfig:
    def __init__(self):
        timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = "HousePricePrediction"
        self.artifact_dir = os.path.join(ARTIFACTS_DIR, timestamp)
        self.timestamp = timestamp

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Raw Data Paths
        self.raw_data_dir: str = file_paths.RAW_DATA_DIR
        self.raw_train_file_path: str = file_paths.RAW_TRAIN_FILE_PATH
        # self.raw_test_file_path: str = RAW_TEST_FILE_PATH

        # Main data ingestion directory
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, file_paths.DATA_INGESTION_DIR)

        # Feature store directory
        self.feature_store_dir: str = os.path.join(self.data_ingestion_dir, file_paths.DATA_INGESTION_FEATURE_STORE)

        # Ingested data directory
        self.ingested_dir: str = os.path.join(self.data_ingestion_dir,file_paths.DATA_INGESTION_INGESTED_DIR)

        # Output train and test file paths for ingested data
        self.ingested_train_file_path: str =os.path.join(self.ingested_dir, file_paths.TRAIN_FILE_PATH)
        self.ingested_test_file_path: str = os.path.join(self.ingested_dir, file_paths.TEST_FILE_PATH)

        # Schema file path
        

class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig, data_ingestion_config: DataIngestionConfig):

    #TODO: 1. Set the data_validation dir path
    # 2. Set the validated data dir path
    # 3. Set the Invalid data dir path
    # 4. Set the drift_report yaml file dir path
    # 5. Set the schema file path
    # 6. Set or collect the train and test file part from the DataIngestionArtifact


        # 1. Set the data_validation dir path
        self.validation_dir = os.path.join(training_pipeline_config.artifact_dir, file_paths.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir = os.path.join(self.validation_dir, file_paths.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir = os.path.join(self.validation_dir, file_paths.DATA_VALIDATION_INVALID_DIR)
        
        # 2. Set validated data dir path for train and test
        self.valid_train_path = os.path.join(self.validation_dir, file_paths.TRAIN_FILE_PATH)
        self.valid_test_path = os.path.join(self.validation_dir, file_paths.TEST_FILE_PATH)

        # 3. Set invalid data dir path
        self.invalid_train_path = os.path.join(self.validation_dir, file_paths.TRAIN_FILE_PATH)
        self.invalid_test_path = os.path.join(self.validation_dir, file_paths.TEST_FILE_PATH)

        # 4. Set the drift_report yaml file dir path
        self.drift_report_file_path: str = os.path.join(
            self.validation_dir, 
            file_paths.DATA_VALIDATION_DRIFT_REPORT_DIR,
            file_paths.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
         )

        # 5. Set the schema file path 
        self.schema_file_path = os.path.join(SCHEMA_DIR, "schema.yaml")

        # 6. Collect the train and test file path from the DataIngestionArtifact
        self.train_file_path = data_ingestion_config.ingested_train_file_path
        self.test_file_path = data_ingestion_config.ingested_test_file_path

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, file_paths.DATA_TRANSFORMATION_DIR_NAME)

        self.transformed_train_file_path: str = os.path.join(self.data_transformation_dir, file_paths.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        file_paths.TRAIN_FILE_PATH.replace("csv", "npy"))

        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir, file_paths.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        file_paths.TEST_FILE_PATH.replace("csv", "npy"))

        self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir, file_paths.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
        file_paths.PREPROCESSING_OBJECT_FILE_NAME)

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, file_paths.MODEL_TRAINER_TRAINED_MODEL_DIR)
        self.model_trained_file_path: str = os.path.join(
        self.model_trainer_dir,
        file_paths.MODEL_TRAINER_TRAINED_MODEL_DIR,
        file_paths.MODEL_TRAINER_TRAINED_MODEL_NAME
        )
        self.model_trainer_expected_r2_score: float = file_paths.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold: float = 0.05


