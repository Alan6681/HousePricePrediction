import os
import pandas as pd
import sys
from housepriceprediction.exception.exception import HousePricePredictionException
from housepriceprediction.logging.logger import logging
import yaml

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path, "rb") as ymal_file:
            return yaml.safe_load(ymal_file)
    except Exception as e:
        raise HousePricePredictionException(e,sys)


def write_yaml_file(file_path:str, content:object, replace:bool=False):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        raise HousePricePredictionException(e,sys)


def save_data_to_feature_store(feature_store_dir: str, df: pd.DataFrame, file_name: str ="feature_store.csv"):
    """
    Saves a list of DataFrames into a single CSV file in the feature store directory.

    Args:
        feature_store_dir (str): Path to the feature store directory.
        df: DataFrame to save.
        file_name (str): Name of the CSV file. Defaults to 'feature_store.csv'.

    Returns:
        str: Full path to the saved feature store CSV file.

    """
    try:
        os.makedirs(feature_store_dir, exist_ok=True) # Check if directory exists if not make it
        feature_store_path = os.path.join(feature_store_dir, file_name) # Creates the path for the feature_store.csv
        df.to_csv(feature_store_path, index=False) # Exporting the dataframe as a csv file, to the path of the feature_store.csv

        return feature_store_path
    except Exception as e:
        raise HousePricePredictionException(e, sys)

