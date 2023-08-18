from processing_script import get_csv
from load_script import load_csv_to_minio

car_list = [("Toyota", "Rav4"), ("Toyota","Land Cruiser Prado"), ("Kia", "Sportage")]
folder_path = 'CSV/'
container = 'raw/'

# for car in car_list:
#     get_csv(car[0], car[1])


load_csv_to_minio(folder_path, container)