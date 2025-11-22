
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
        feature_store_file_path: str
        train_file_path: str
        test_file_path: str

@dataclass
class DataValidationArtifact:
        valid_train_df: str
        valid_test_df:str
        invalid_train_df: str 
        invalid_test_df:str
        drift_report_file_path: str
        validation_status : bool

@dataclass
class DataTransformationArtifact:
        transformed_train_file_path: str
        transformed_test_file_path: str
        preprocessed_object_file_path: str

@dataclass
class RegressionMetricArtifact:
        r2_score: float
        root_mean_squared_error: float

@dataclass
class ModelTrainerArtifact:
        trained_model_file_path: str
        train_metric_artifact: RegressionMetricArtifact
        test_metric_artifact: RegressionMetricArtifact
        is_model_accepted: bool
   



    
    
        
    
    

