from scripts.processing_script import get_csv
from scripts.load_script import load_csv_to_minio

car_list = [("Toyota", "Rav4"), ("Toyota","Land Cruiser Prado"), ("Kia", "Sportage")]
folder_path = 'CSV/'
container = 'raw/'

if __name__ == "__main__":
    for car in car_list:
        get_csv(car[0], car[1])

    load_csv_to_minio(folder_path, container)


