import polars as pl
from scrapper import get_car_data

def get_dataframe(index: int):

    try:
        table_data = get_table_data(url, index)
        print("Column data and Row data was successfully collected...")

        table_names = table_data[0]
        table_row_data = table_data[1][1:]

        df = pl.DataFrame(table_row_data, schema=table_names)
        print("Polars Dataframe has been created")
        return df

    except Exception as e:
        print("An unexpected error occurred:", e)

