from minio import Minio, S3Error
from dotenv import load_dotenv
import os

load_dotenv()

minio_endpoint = os.getenv('MINIO_ENDPOINT')
minio_access_key = os.getenv('MINIO_ACCESS_KEY')
minio_secret_key = os.getenv('MINIO_SECRET_KEY')
minio_bucket_name = os.getenv('MINIO_BUCKET_NAME')

def load_csv_to_minio(folder_path, container):

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


