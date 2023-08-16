from bs4 import BeautifulSoup
import requests
import math

car_brand = "Toyota"
car_model = "Land Cruiser Prado"

# url = f'https://www.supercarros.com/carros/cualquier-tipo/cualquier-provincia/{car_brand}/{car_model}/?PagingPageSkip=0'

def get_number_of_pages():

    url = f'https://www.supercarros.com/carros/cualquier-tipo/cualquier-provincia/{car_brand}/{car_model}/?PagingPageSkip=0'
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    return int(math.ceil(float(soup.find('strong', id="LowerCounter2").text)/24))


def get_car_data():
    # url = f'https://www.supercarros.com/carros/cualquier-tipo/cualquier-provincia/{car_brand}/{car_model}/?PagingPageSkip={num_pages}'
    cars_per_page = []

    for num_pages in range(get_number_of_pages()):
        url = f'https://www.supercarros.com/carros/cualquier-tipo/cualquier-provincia/{car_brand}/{car_model}/?PagingPageSkip={num_pages}'

        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')


        results_div = soup.find('div', id='bigsearch-results-inner-results')

        results_ul = results_div.find('ul')

        results_list = results_ul.find_all('li')


        for li in results_list:
            price = li.find('div', class_="price").text
            year = li.find('div', class_="year").text
            model_trim = li.find('div', class_="title1").text
            description = li.find('div', class_="title2").text.strip()

            car_object = {"Price": price, "Year": year, "Model-Trim": model_trim, "Description": description}
            cars_per_page.append(car_object)

    return cars_per_page
