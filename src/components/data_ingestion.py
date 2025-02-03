
import os 
import sys 
sys.path.append(os.path.join(os.getcwd(), 'src'))
import pandas as pd 
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Access the Data Ingestion Method or Component")
        try:
            # Here are loading the data from the csv and dumping into the variable name ""
            df = pd.read_csv("notebook\\Data\\stud.csv")  # Escaping backslashes
            logging.info("Load and Access the Data Successfully")
            
            #Here we are creating the "artifacts" folder and  Ensure the folder exists before saving the train.csv, test.csv and data.csv file later in the code.
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            #saving the DataFrame df to a CSV file at the location specified by raw_data_path (which is 'artifacts/data.csv')
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info("Raw data is saved in the data.csv")

            #Splits the DataFrame df into 80% training and 20% testing data.
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            logging.info("Train test split initiated ")
            #saving the spilited DataFrame df to a CSV file at the location specified by test_data_path (which is 'artifacts/test.csv')
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info("test.csv is build successfully")
            #saving the spilited DataFrame df to a CSV file at the location specified by trainst_data_path (which is 'artifacts/train.csv)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            logging.info("train.csv is build successfully")

            logging.info("Imgestion of the data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()




