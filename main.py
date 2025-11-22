from housepriceprediction.components.data_ingestion import DataIngestion
from housepriceprediction.components.data_validation import DataValidation
from housepriceprediction.components.data_transformation import DataTransformation
from housepriceprediction.components.model_trainer import ModelTrainer

from housepriceprediction.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from housepriceprediction.entity.artifacts_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from housepriceprediction.exception.exception import HousePricePredictionException
from housepriceprediction.logging.logger import logging
import sys


def run_training_pipeline():

    try:
        # -----------------------------------------
        # STEP 1 — TRAINING PIPELINE CONFIG
        # -----------------------------------------
        pipeline_config = TrainingPipelineConfig()
        logging.info("Training Pipeline Config Loaded")

        # -----------------------------------------
        # STEP 2 — DATA INGESTION
        # -----------------------------------------
        ingestion_config = DataIngestionConfig(pipeline_config)
        ingestion = DataIngestion(ingestion_config)

        ingestion_artifact = ingestion.initiate_ingestion()
        logging.info("Data Ingestion Completed")

        # -----------------------------------------
        # STEP 3 — DATA VALIDATION
        # -----------------------------------------
        validation_config = DataValidationConfig(
            training_pipeline_config=pipeline_config,
            data_ingestion_config=ingestion_config
        )

        validation = DataValidation(
            data_ingestion_artifact=ingestion_artifact,
            data_validation_config=validation_config
        )

        validation_artifact = validation.initiate_data_validation()
        logging.info("Data Validation Completed")

        # -----------------------------------------
        # STEP 4 — DATA TRANSFORMATION
        # -----------------------------------------
        transformation_config = DataTransformationConfig(pipeline_config)

        transformation = DataTransformation(
            data_validation_config=validation_config,
            data_validation_artifact=validation_artifact,
            data_transformation_config=transformation_config
        )

        transformation_artifact = transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")

        # -----------------------------------------
        # STEP 5 — MODEL_TRAINER
        # -----------------------------------------

        model_trainer_config = ModelTrainerConfig(training_pipeline_config=pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model_Trainer completed")

        print("Training pipeline completed")



        return {
            "ingestion": ingestion_artifact,
            "validation": validation_artifact,
            "transformation": transformation_artifact,
            "model_trainer" : model_trainer_artifact
        }



    except Exception as e:
        raise HousePricePredictionException(e, sys)


if __name__ == "__main__":
    run_training_pipeline()
