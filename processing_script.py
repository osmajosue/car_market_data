import polars as pl
from scrapper import get_car_data


def get_dataframe():

    try:
        car_data = get_car_data()
        print("Car Data data was successfully collected...")

        schema = ["Precio", "Marca", "Modelo", "Año", "Motor", "Color Exterior", "Tipo", "Color Interior", "Uso", "Combustible", "Carga", "Transmision", "Puertas", "Traccion", "Pasajeros"]

        df = pl.DataFrame(car_data, schema=schema)
        print("Polars Dataframe has been created")

        df = df.with_row_count()
        df = df.rename({"row_nr": "id"})

        return df

    except Exception as e:
        print("An unexpected error occurred:", e)

df = get_dataframe()

print(df.head(50))

