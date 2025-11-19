import os
import sys
import pandas as pd
from housepriceprediction.entity.artifacts_entity import DataIngestionArtifact
from housepriceprediction.entity.config_entity import DataIngestionConfig
from housepriceprediction.logging.logger import logging
from housepriceprediction.exception.exception import HousePricePredictionException
from housepriceprediction.utils.main_utils.utils import save_data_to_feature_store


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


            # 1. Load the train and test files from the raw file path
            df_train = pd.read_csv(self.data_ingestion_config.raw_train_file_path)
            df_test = pd.read_csv(self.data_ingestion_config.raw_test_file_path)
            logging.info("Raw files loaded successfully")

            # 2. Save the data to feature store
            feature_store_path = save_data_to_feature_store(df_list=[df_train, df_test], feature_store_dir=self.data_ingestion_config.feature_store_dir)
            logging.info("Raw data saved to feature_store.csv successfully")

            # 3. Save the ingested train/test files to ingested dir
            df_train.to_csv(self.data_ingestion_config.ingested_train_file_path, index=False)
            df_test.to_csv(self.data_ingestion_config.ingested_test_file_path, index=False)
            logging.info("Ingested train and test file saved successfully")

            # 4. Return DataIngestionArtifact
            data_ingestion_artifact =  DataIngestionArtifact(feature_store_file_path=feature_store_path, train_file_path=self.data_ingestion_config.ingested_train_file_path, test_file_path=self.data_ingestion_config.ingested_test_file_path)
            logging.info("DataIngestion Artifact Created")

            return data_ingestion_artifact
        except Exception as e:
            raise HousePricePredictionException(e,sys)