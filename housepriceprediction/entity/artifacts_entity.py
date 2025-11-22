import os

class DataIngestionArtifact:
    def __init__(self, feature_store_file_path: str, train_file_path: str, test_file_path: str):
        self.feature_store_file_path = feature_store_file_path
        self.train_file_path = train_file_path
        self.test_file_path = test_file_path

class DataValidationArtifact:
    def __init__(self,  valid_train_df:str, valid_test_df: str, invalid_train_df: str, invalid_test_df: str, drift_report_file_path: str, validation_status: bool):
        self.valid_train_df = valid_train_df
        self.valid_test_df = valid_test_df
        self.invalid_train_df = invalid_train_df
        self.invalid_test_df = invalid_test_df
        self.drift_report_file_path = drift_report_file_path
        self.validation_status = validation_status

class DataTransformationArtifact:
    def __init__(self, transformed_train_file_path:str, transformed_test_file_path:str, preprocessed_object_file_path:str):
        self.transformed_train_file_path = transformed_train_file_path
        self.transformed_test_file_path = transformed_test_file_path
        self.preprocessed_object_file_path = preprocessed_object_file_path



    
    
        
    
    

