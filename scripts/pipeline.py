
from scripts.processing_script import get_csv
from scripts.load_script import load_csv_to_minio, load_csv_to_db
import os

car_list = [("Toyota", "Rav4"), ("Toyota","Land Cruiser Prado"), ("Honda", "CRV"), ("Kia", "Sportage")]
folder_path = 'CSV/'
container = 'raw/'
file_list = os.listdir(folder_path)

def ingestion_pipeline():
    for car in car_list:
        get_csv(car[0], car[1])


def load_pipeline():  
    load_csv_to_db(folder_path, file_list)
    load_csv_to_minio(folder_path, container)