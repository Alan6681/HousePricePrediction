import os
import pandas as pd
import sys
from housepriceprediction.exception.exception import HousePricePredictionException
from housepriceprediction.logging.logger import logging
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import pickle
import yaml
import numpy as np

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

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file 
    file_path:str location of file to save 
    array: np.array data to save

    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
       raise HousePricePredictionException(e,sys) 
    
def load_numpy_array(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    
    """
    if not os.path.exists(file_path):
        raise Exception(f"Numpy array file path {file_path} does not exist")
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise HousePricePredictionException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            gs = GridSearchCV(model, para, cv=2, n_jobs=-1)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            #model.fit(X_train, y_train) # Train model

            y_train_preds = model.predict(X_train)
            y_test_preds = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_preds)
            test_model_score = r2_score(y_test, y_test_preds)

            report[list(models.keys())[i]] = test_model_score

        return report
    except Exception as e:
        raise HousePricePredictionException(e, sys)
            


def save_object(file_path: str, obj:object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise HousePricePredictionException(e,sys)
    
def load_object(file_path: str)-> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise HousePricePredictionException(e, sys)


        

