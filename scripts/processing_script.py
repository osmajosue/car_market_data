import polars as pl
import pandas as pd
from scripts.scrapper import get_car_data
from datetime import date
from scripts.utils import time_func


@time_func
def get_polars_dataframe(*args):

    try:
        car_data = get_car_data(args[0], args[1])
        print(f"Car Market Data for {args[0]} {args[1]} was successfully collected...")

        schema = ["Precio", "Marca", "Modelo", "Año", "Motor", "ColorExterior", "Tipo", "ColorInterior", "Uso", "Combustible", "Carga", "Transmision", "Puertas", "Traccion", "Pasajeros"]

        df = pl.DataFrame(car_data, schema=schema)
        print("Polars Dataframe has been created")

        df = df.with_row_count()
        df = df.rename({"row_nr": "id"})

        return df

    except Exception as e:
        print("An unexpected error occurred:", e)


@time_func
def get_pandasdf_from_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print("An unexpected error occurred:", e)


@time_func
def get_csv(*args):

    name = f"{args[0]} {args[1]}"

    df = get_polars_dataframe(args[0], args[1])
    current_date = date.today()
    file_path = f"CSV/{current_date}_{name}.csv"
    
    try:
        df.write_csv(file_path)
        print(f"The CSV for the {name} dataframe has been created successfully on -> {current_date}")
    except Exception as e:
        print("An unexpected error occurred:", e)

