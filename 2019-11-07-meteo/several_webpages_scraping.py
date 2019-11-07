""""
Scrape weather infos from a several web page of www.infoclimat.fr
data is written in a csv file, that will be use to check info from other sources
Author : Olivier Brunet
2019-11-07
Licence : GPL
"""

import pickle, os, csv, requests, datetime
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from fake_useragent import UserAgent
from random import randint
from time import sleep


file_name_pickle, file_name_csv = 'scraped_page.pickle', 'scraped_data.csv'
days, months_nb, years = list(range(1, 32)), list(range(1, 12)), [2016, 2017, 2018, 2019]
months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre'\
          'octobre', 'novembre', 'decembre']


def retrieve_webpage(page_url):
    """Get a webpage with the requests module & return the response"""
    # if the page has already been downloaded & saved
    if os.path.exists(file_name_pickle):
        with open(file_name_pickle, 'rb') as f:
            print(f"Loading cached {file_name_pickle}")
            response = pickle.load(f)
    # otherwise fetch it for the first time
    else:
        print(f"Fetching {page_url} from the internet")
        try:
            headers = {'User-Agent': UserAgent().random}
            response = requests.get(page_url, headers=headers)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None
        else:
            print('Request success!')
            with open(file_name_pickle, 'wb') as f:
                print(f"Writing cached {file_name_pickle}")
                pickle.dump(response, f)
            return response


def get_response_data(resp, date):
    """Parse HTTP response of a single webpage with BS4 and return relevant data"""
    soup = BeautifulSoup(resp.text, 'html5lib')
    # classes range from class_='cdata-hour23' for 00h to class_='cdata-hour00' for 1h
    hr_range = [f"{i:02d}" for i in list(range(23, -1, -1)) ]
    data = ""
    for h in hr_range:
        class_ = 'cdata-hour' + h
        try:
            row = soup.find('tr', class_= class_)
        except:
            continue
        try:
            hour = row.find('span', class_="tipsy-trigger").text
        except:
            hour = 'NaN'
        try:
            temp = row.find('span', text="°C", attrs={'class': 'tab-units-v'}).previous_sibling.previous_sibling.text
        except:
            temp = 'NaN'
        try:
            rain = row.find('span', text="mm/1h", attrs={'class': 'tab-units-v'}).find_parent('td').contents[0].replace(' ', '')
        except:
            rain = 'NaN'
        try:
            humi = row.find('span', text="%", attrs={'class': 'tab-units-v'}).previous_sibling.text
        except:
            humi = 'NaN'
        try:
            wind = row.find('span', text="km/h", attrs={'class': 'tab-units-v'}).previous_sibling.previous_sibling.text
        except:
            wind = 'NaN'
        result = ';'.join([date, hour, temp, rain, humi, wind]) + '\n'
        data += result
    return data


if __name__ == "__main__":
    csv_header = "date;heure;temperature(°C);pluie(mm/1h);humidite(%);vent_moyen(km/h)\n"
    with open(file_name_csv, 'w') as f:
        f.write(csv_header)
    for y in years:
        for m in months_nb:
            for d in days:
                try:
                    current_date = datetime.datetime(y, m, d)
                # if current_date isn't a valid date
                except ValueError:
                    continue
                # check is date is in the future !!!!!!!!!!!!!!!!!!!!!!!


                # wait a random amount of time to mimic human behavior, before a new web page request
                sleep(randint(2, 15))
                page_url = f"https://www.infoclimat.fr/observations-meteo/archives/{d}/{months[m-1]}/{y}/paris-montsouris/07156.html"
                response = retrieve_webpage(page_url)
                page_data = get_response_data(response, current_date)
                with open(file_name_csv, 'a') as f:
                    f.write(page_data)
