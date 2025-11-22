import os

# Base Folders

ARTIFACTS_DIR: str = "artifacts"
RAW_DATA_DIR: str = "HousePrice_data"
TRAIN_FILE_PATH: str = "train.csv"
TEST_FILE_PATH: str = "test.csv"
SCHEMA_DIR: str = "data_schema"



# Paths to raw data
RAW_TRAIN_FILE_PATH: str = os.path.join(RAW_DATA_DIR, TRAIN_FILE_PATH)
RAW_TEST_FILE_PATH: str = os.path.join(RAW_DATA_DIR, TEST_FILE_PATH)


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME

"""

DATA_INGESTION_DIR: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"



"""
Data Validation related constant start with DATA_VALIDATION VAR NAME

"""

DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing_object.pkl"



"""
Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME

"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"

#KNN imputer to replace nan values
DATA_TRANSFORMED_IMPUTER_PARAMS = {
    "n_neighbors": 3,
    "weights": "uniform"
}
 
"""
Model Trainer related constant start with MODEL_TRAINER VAR NAME

"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "house_price_model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.7
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD: float = 0.05





