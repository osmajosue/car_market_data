import polars as pl
from scrapper import get_car_data

url = f'https://www.supercarros.com/carros/cualquier-tipo/cualquier-provincia/Toyota/RAV4/?PagingPageSkip=0'


def get_dataframe():

    try:
        car_data = get_car_data(url)
        print("Car Data data was successfully collected...")

        schema = ["Price", "Year", "Model-Trim", "Description"]

        df = pl.DataFrame(car_data, schema=schema)
        print("Polars Dataframe has been created")

        df = df.with_row_count()
        df = df.rename({"row_nr": "id"})

        return df

    except Exception as e:
        print("An unexpected error occurred:", e)

df = get_dataframe()

print(df.head(5))

