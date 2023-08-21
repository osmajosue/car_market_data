from minio import Minio, S3Error
from dotenv import load_dotenv
from scripts.db_connection import db_connection_engine
import os
from scripts.utils import time_func
from scripts.processing_script import get_pandasdf_from_csv


@time_func
def load_csv_to_minio(folder_path, container):
    load_dotenv()

    minio_endpoint = os.getenv('MINIO_ENDPOINT')
    minio_access_key = os.getenv('MINIO_ACCESS_KEY')
    minio_secret_key = os.getenv('MINIO_SECRET_KEY')
    minio_bucket_name = os.getenv('MINIO_BUCKET_NAME')

    minio_client = Minio(minio_endpoint,
                        access_key=minio_access_key,
                        secret_key=minio_secret_key,
                        secure=False) 

    try:
        if not minio_client.bucket_exists(minio_bucket_name):
            minio_client.make_bucket(minio_bucket_name)
            print(f"Bucket '{minio_bucket_name}/{container}' created.")
    except S3Error as e:
        print(f"Error: {e}")

    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    for file in files:
        file_path = os.path.join(folder_path, file)
        object_name = container + os.path.basename(file_path)
        
        minio_client.fput_object(minio_bucket_name, object_name, file_path)

    print(f"{len(files)} .csv files uploaded to MinIO bucket '{minio_bucket_name}/{container}'.")


def load_csv_to_db(folder_path, file_list):
    for file_name in file_list:
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(folder_path, file_name)
            df = get_pandasdf_from_csv(csv_file_path)

            file_name_without_extension = os.path.splitext(file_name)[0]

            last_underscore_index = file_name_without_extension.rfind('_')

            table_name = file_name_without_extension[last_underscore_index + 1:].replace(" ", "")

            create_table_schema(table_name, df)
            load_to_database(table_name, df)

@time_func
def create_table_schema(table_name, df):
    db_engine = db_connection_engine()
    try:
        df.head(n=0).to_sql(name=table_name, con=db_engine, if_exists="replace")
        print("Table Schema created!")
    except:
        print("Error connecting to the db")

@time_func
def load_to_database(table_name, df):
    db_engine = db_connection_engine()
    try:
        df.to_sql(name=table_name, con=db_engine, if_exists="append")
        print("Data loaded successfully to the db")
    except:
        print("Error loading data to the database...")
    print("Data loaded succesfully...")
