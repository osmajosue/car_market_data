from bs4 import BeautifulSoup
import requests
import math
from dotenv import load_dotenv
import os
from scripts.utils import time_func


load_dotenv()

base_url = os.getenv("BASE_URL")

@time_func
def get_number_of_pages(*args):
    
    url = f'{base_url}/carros/cualquier-tipo/cualquier-provincia/{args[0]}/{args[1]}/?PagingPageSkip=0'
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    num_pages_text = soup.find('strong', id="LowerCounter2").text
    print(num_pages_text)

    if num_pages_text == "1,000+":
        num_pages = 42
    else:
        num_pages = int(math.ceil(float(num_pages_text)/24))
    
    return num_pages

@time_func
def get_car_data(*args):

    number_of_pages = get_number_of_pages(args[0], args[1])
    cars_per_page = []

    for num_pages in range(number_of_pages):
        url = f'{base_url}/carros/cualquier-tipo/cualquier-provincia/{args[0]}/{args[1]}/?PagingPageSkip={num_pages}'

        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')


        results_div = soup.find('div', id='bigsearch-results-inner-results')

        results_ul = results_div.find('ul')

        results_list = results_ul.find_all('li')


        for li in results_list:

            link = str(li.a.get("href"))

            link_response = requests.get(base_url+link)

            soup = BeautifulSoup(link_response.text, 'html.parser')

            car_model_header = soup.find('div', id="detail-ad-header")

            car_model_h1 = car_model_header.find('h1').text

            table = soup.find('table')

            table_rows = []

            rows = table.find_all('tr')

            car_dict = {}
            for row in rows:
                row_data = row.find_all('td')
                individual_row_data = [data.text.strip() for data in row_data]

                table_rows.append(individual_row_data)

                
                for item in table_rows:
                    if len(item) <= 2:
                        key = item[0].rstrip(':')
                        value = item[1]
                        car_dict[key] = value
                    else:
                        key = item[0].rstrip(':')
                        value = item[1]
                        car_dict[key] = value

                        key2 = item[2].rstrip(':')
                        value2 = item[3]
                        car_dict[key2] = value2

                    car_dict["Marca"] = args[0]
                    car_dict["Modelo"] = args[1]
                    car_dict["Año"] = car_model_h1[-4:]

            cars_per_page.append(car_dict)
            
    return cars_per_page