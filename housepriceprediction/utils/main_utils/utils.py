import os
import pandas as pd
import sys
from housepriceprediction.exception.exception import HousePricePredictionException
from housepriceprediction.logging.logger import logging

def save_data_to_feature_store(feature_store_dir: str, df_list: list, file_name: str ="feature_store.csv"):
    """
    Saves a list of DataFrames into a single CSV file in the feature store directory.

    Args:
        feature_store_dir (str): Path to the feature store directory.
        df_list (list): List of DataFrames to concatenate and save.
        file_name (str): Name of the CSV file. Defaults to 'feature_store.csv'.

    Returns:
        str: Full path to the saved feature store CSV file.

    """
    try:
        os.makedirs(feature_store_dir, exist_ok=True) # Check if directory exists if not make it
        feature_store_path = os.path.join(feature_store_dir, file_name) # Creates the path for the feature_store.csv
        df = pd.concat(df_list, ignore_index=True) # Combine both the train and test data into one dataframe
        df.to_csv(feature_store_path, index=False) # Exporting the dataframe as a csv file, to the path of the feature_store.csv

        return feature_store_path
    except Exception as e:
        raise HousePricePredictionException(e, sys)

