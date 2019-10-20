"""get all pokemons' names & infos from the web page https://pokemondb.net and all its links,
 then save results in a csv file for later analysis with a jupyter notebook"""

# problems with encoding due to 2 words names, and don't write line by line...

import os, requests, pickle, html5lib
from bs4 import BeautifulSoup


BASE_URL = 'https://pokemondb.net'
file_name = 'scraped_pokemon_page.pickle'
# all parsed infos = columns' names of the csv file


def scrape_general_page(base_url):
    """Scrape the web page with general infos on all pokemon then if succeed, write a binary file for later use
    receive a URL - return request's result """
    if not os.path.exists(file_name):
        result = requests.get(base_url + "/pokedex/national")
        assert result.status_code == 200, print(f'Attempt to retrieve web page failed - result code {result.status_code}')
        with open(file_name, 'wb') as f:
            pickle.dump(result, f)
    else:
        with open(file_name, 'r') as f:
            result = pickle.load(f)
    return result


def create_bs4_object(result):
    """Receive a request's result & return a created bs4 object for parsing infos"""
    return BeautifulSoup(result.content, 'html5lib')


def get_gen_infos(ic):
    """Receive a specific infocard & return general infos parsed"""
    gen_infos = ic.get_text().split()
    if len(gen_infos) == 3:                                                                     # only one type
        id_nb, name, type_1, type_2 = gen_infos[0], gen_infos[1], gen_infos[2], "Nan"
    elif len(gen_infos) == 5:                                                                   # with two types
        id_nb, name, type_1, type_2 = gen_infos[0], gen_infos[1], gen_infos[2], gen_infos[4]
    else:                                                                                       # if a problem occurs
        id_nb = name = type_1 = type_2 = "Nan"
    link = ic.a.get('href')
    return id_nb, name, type_1, type_2, link


def get_stats(soup):
    data_species = soup.find("th", text="Species").next_sibling.next_sibling.string
    data_height = soup.find("th", text="Height").next_sibling.next_sibling.string.split()[0]
    data_weight = soup.find("th", text="Weight").next_sibling.next_sibling.string.split()[0]
    data_abilities = soup.find("th", text="Abilities").next_sibling.next_sibling.a.text
    training_catch_rate = soup.find("th", text="Catch rate").next_sibling.next_sibling.text.split()[0]
    training_base_exp = soup.find("th", text="Base Exp.").next_sibling.next_sibling.text
    training_growth_rate = soup.find("th", text="Growth Rate").next_sibling.next_sibling.text
    breeding_gender = soup.find("th", text="Gender").next_sibling.next_sibling.text
    stats_hp = soup.find("th", text="HP").next_sibling.next_sibling.text
    stats_attack = soup.find("th", text="Attack").next_sibling.next_sibling.text
    stats_defense = soup.find("th", text="Defense").next_sibling.next_sibling.text
    stats_sp_atk = soup.find("th", text="Sp. Atk").next_sibling.next_sibling.text
    stats_sp_def = soup.find("th", text="Sp. Def").next_sibling.next_sibling.text
    stats_speed = soup.find("th", text="Speed").next_sibling.next_sibling.text
    stats_total = soup.find("th", text="Total").next_sibling.next_sibling.text
    return data_species, data_height, data_weight, data_abilities, training_catch_rate, training_base_exp, \
           training_growth_rate, breeding_gender, stats_hp, stats_attack, stats_defense, stats_sp_atk, stats_sp_def, \
           stats_speed, stats_total


def parse_infocards(soup, pokemon_infos):
    """Receive the bs4 object of the main page, parse all infocards and call others func to retrieve infos
    Return a coma separated string of the whole db"""
    all_db = ""

    # get a list of all infocards
    infocards = soup.find_all("div", class_="infocard")                     # test print(infocards[0].prettify())

    for ic in infocards:
        gen_infos = list(get_gen_infos(ic))
        # request for linked page to get specific stats
        r = requests.get(BASE_URL + gen_infos[-1])
        if r.status_code != 200:
            st = "\n" + ";".join(gen_infos) + ";Nan" * (len(pokemon_infos) - len(gen_infos))
        else:
            other_soup = BeautifulSoup(r.content, 'html5lib')
            stats = list(get_stats(other_soup))
            st = "\n" + ";".join(gen_infos) + ";".join(stats)
        all_db += st + "\n"

    return all_db


def main():
    result = scrape_general_page(BASE_URL)
    soup = create_bs4_object(result)

    pokemon_infos = """id_nb;name;type_1;type_2;link;data_species;data_height;data_weight;data_abilities;training_catch_rate;
    training_base_exp;training_growth_rate; breeding_gender;stats_hp;stats_attack;stats_defense; stats_sp_atk;stats_sp_def;
    stats_speed;stats_total;"""

    pokemon_infos += parse_infocards(soup, pokemon_infos)
    with open("pokemon_db.csv", 'wb') as f:
        f.write(pokemon_infos)


if __name__ == "__main__":
    main()