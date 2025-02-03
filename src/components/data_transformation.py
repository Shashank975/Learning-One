import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Import Other Py Files
sys.path.append(os.path.join(os.getcwd(), 'src'))
from ..logger import logging
from ..exception import CustomException
from ..utils import save_object


@dataclass
class DataTranformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTranformationConfig()

    def get_data_transformation_obj(self):
        try:
            numerical_columns = ['reading_score', 'writing_score']
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            # Correct pipeline creation
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler(with_mean=False))
            ])

            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore')),
                ('scaler', StandardScaler(with_mean=False))
            ])

            logging.info(f"Numerical Columns are: {numerical_columns}")
            logging.info(f"Categorical Columns are: {categorical_columns}")

            processor = ColumnTransformer(
                transformers=[
                    ('num_pipeline', num_pipeline, numerical_columns),
                    ('cat_pipeline', cat_pipeline, categorical_columns),
                ]
            )

            return processor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Load data
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            logging.info("Data Got Readed")

            # Get Data Transformation Object
            processing_obj = self.get_data_transformation_obj()

            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df = train_data.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_data[target_column_name]

            input_feature_test_df = test_data.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_data[target_column_name]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe.")

            input_feature_train_arr = processing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = processing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=processing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
            logging.error(f"An error occurred in data transformation: {e}")



# import sys
# import os
# sys.path.append('C:/Users/LENOVO/Desktop/Personal Work/Learning-One')
# print(sys.path)


# import sys
# import os
# sys.path.append('C:/Users/LENOVO/Desktop/Personal Work/Learning-One')
# from src.utils import save_object  # Test this import


