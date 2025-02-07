import os
import sys
from dataclasses import dataclass

# Import models and necessary libraries
from xgboost import XGBRegressor  # Replacing CatBoost with XGBoost
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

# Import custom exception, logger, and utility functions
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

# Configuration class to store the model path
@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test data into input and output")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )
            
            # Define models
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),  # Using XGBRegressor instead of CatBoost
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            
            

            # Get model performance report without hyperparameter tuning
            model_report = {}
            for model_name, model in models.items():
                model.fit(X_train, y_train)
                score = model.score(X_test, y_test)
                model_report[model_name] = score
            
            # Find the best model from the report
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]
            best_model_score = model_report[best_model_name]

            # Check if the best model score is acceptable
            if best_model_score < 0.6:
                raise CustomException("No suitable model found")

            logging.info(f"Best model: {best_model_name} with score {best_model_score}")

            # Save the best model
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=best_model)

            # Predict and evaluate the model on test data
            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)

            return r2_square

        except Exception as e:
            raise CustomException(e, sys)
