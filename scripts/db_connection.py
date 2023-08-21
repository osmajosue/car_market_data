from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from scripts.utils import time_func

load_dotenv()


@time_func
def db_connection_engine():

    db=os.getenv("_DB")
    db_user=os.getenv("DB_USER")
    db_pass=os.getenv("DB_PASSWORD")
    db_host=os.getenv("DB_HOST")
    db_port=os.getenv("DB_PORT")
    db_name=os.getenv("DB_NAME")

    try:
        db_engine = create_engine(
            f"{db}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
        print("The connection to the database was successful")
        return db_engine
    except:
        print("Error connecting to the database...")

