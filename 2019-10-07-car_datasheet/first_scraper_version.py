import requests
from bs4 import BeautifulSoup

PATH = 'http://localhost:8000/auto_mpg.html'


def process_car_blocks(soup):
    """Extract infos from repeated divisions"""
    car_blocks = soup.find_all('div', class_='car_block')
    rows = []

    for cb in car_blocks:
        str_name = cb.find('span', class_='car_name').text

        str_cylinders = cb.find('span', class_='cylinders').text
        cylinders = int(str_cylinders)
        assert cylinders > 0, f'Expecting cylinders to be positive not {cylinders}'

        str_weight = cb.find('span', class_='weight').text
        weight = int(str_weight.replace(',', ''))
        assert weight > 0, f'Expecting weight to be positive not {weight}'

        str_from = cb.find('span', class_='from').text
        year, territory = str_from.strip('()').split(',')
        year = int(year.strip())
        assert year > 0 or len(territory) > 0, f'Expecting year to be positive not {year} or territory to be a usefull string {territory}'

        acceleration = float(cb.find('span', class_='acceleration').text)
        assert weight > 0, f'Expecting acceleration to be positive not {acceleration}'

        str_mpg = cb.find('span', class_='mpg').text
        try:
            mpg = float(str_mpg.split(' ')[0])
            assert mpg > 7, f'Expecting reasonable value of mpg not {mpg}'
        except ValueError:
            mpg = 'NULL' # for excel or pandas

        row = dict(name=str_name, cylinders=cylinders, weight=weight, year=year, territory=territory,\
                   acceleration=acceleration, mpg=mpg)
        rows.append(row)

    # sanity check
    print(f'We have {len(rows)} of scraped car data')
    print(rows[0], '\n', rows[-1])


# --- main ---
result = requests.get(PATH)
assert result.status_code == 200, f'Got status code {result.status_code} which is a problem'
soup = BeautifulSoup(result.text, 'html.parser')
process_car_blocks(soup)