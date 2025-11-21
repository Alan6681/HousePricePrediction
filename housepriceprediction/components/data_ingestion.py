import os
import sys
import pandas as pd
from housepriceprediction.entity.artifacts_entity import DataIngestionArtifact
from housepriceprediction.entity.config_entity import DataIngestionConfig
from housepriceprediction.logging.logger import logging
from housepriceprediction.exception.exception import HousePricePredictionException
from housepriceprediction.utils.main_utils.utils import save_data_to_feature_store
import write_schema
from housepriceprediction.constants.file_paths import SCHEMA_DIR
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def initiate_ingestion(self) -> DataIngestionArtifact:
        try:
            # TODO: 1. Load data from raw folder
            # 2. save the data to feature store.
            # 3. save the ingested train/test files to the dir
            # 4. return the DataIngestionArtifact

            # Ensure directories exist
            os.makedirs(self.data_ingestion_config.feature_store_dir, exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.ingested_train_file_path), exist_ok=True)


            # 1. Load the train data raw file path
            df = pd.read_csv(self.data_ingestion_config.raw_train_file_path)
            df.drop(columns=["Id"], inplace=True)
            logging.info("Raw files loaded successfully")

            # 2. Save the data to feature store
            feature_store_path = save_data_to_feature_store(df=df, feature_store_dir=self.data_ingestion_config.feature_store_dir)
            logging.info("Raw data saved to feature_store.csv successfully")

            # Split the data into train and test sets
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            logging.info("Data split into train and test sets successfully")
            


            # 3. Save the ingested train/test files to ingested dir
            train_set.to_csv(self.data_ingestion_config.ingested_train_file_path, index=False)
            test_set.to_csv(self.data_ingestion_config.ingested_test_file_path, index=False)
            logging.info("Ingested train and test file saved successfully")

            # 4. Return DataIngestionArtifact
            data_ingestion_artifact =  DataIngestionArtifact(feature_store_file_path=feature_store_path, train_file_path=self.data_ingestion_config.ingested_train_file_path, test_file_path=self.data_ingestion_config.ingested_test_file_path)
            logging.info("DataIngestion Artifact Created")

            # Write schema file
            os.makedirs(SCHEMA_DIR, exist_ok=True)
            write_schema.dataframe_to_yaml(df, yaml_path=os.path.join(SCHEMA_DIR, "schema.yaml"))

            return data_ingestion_artifact
        except Exception as e:
            raise HousePricePredictionException(e,sys)