- 2019-10-07 - [Car Datasheet (1970-1982)](https://github.com/obrunet/Web_Scraping_Projects/blob/master/2019-10-07-car_datasheet/auto_mpg.html) - Basics of scraping using bs4, first try with [a notebook](https://github.com/obrunet/Web_Scraping_Projects/blob/master/2019-10-07-car_datasheet/scraping%20data.ipynb), then using [a robust script written with pycharm](https://github.com/obrunet/Web_Scraping_Projects/blob/master/2019-10-07-car_datasheet/last_scraper_version.py), and finally an [exploratory data analysis](https://github.com/obrunet/Web_Scraping_Projects/blob/master/2019-10-07-car_datasheet/making_scraped_data_usable.ipynb) with pandas and seaborn

- 2019-10-20 - [Pokemon's database](https://pokemondb.net/) - a little more complicated scraping task using bs4, different first tries are made with the notebooks in the directory but the main and final script with pycharm is [HERE](https://github.com/obrunet/Web_Scraping_Projects/blob/master/2019-10-20-pokemon_db/main.py). Then i've started to make a [statisctical analysis](https://github.com/obrunet/Web_Scraping_Projects/blob/master/2019-10-20-pokemon_db/pokemon_stats.ipynb) but it's uncomplete, i'll finished later if i've time :)

- 2019-11-07 - [Historical climate & meteo data](www.infoclimat.fr) - advanced scraping using different ways and technics to retrieve data with bs4, first tries with a jupyter [notebook](https://github.com/obrunet/Web_Scraping_Projects/blob/master/2019-11-07-meteo/meteo_scraping.ipynb), the final python script can be found [here](https://github.com/obrunet/Web_Scraping_Projects/blob/master/2019-11-07-meteo/several_webpages_scraping.py) it makes use of FakeUserAgent to forge requests with random realistic browser's headers. I've also use sleep intervals between requests of a random nb of seconds. Finally, the script is quite robust, all cases are managed, missing values, http errors...

---
More to come in the next weeks:
- retrieve news' titles of tabloid or online newspapers
- scrape tweets message
- get top 250 movies on IMDB
- download every link on a specific webpage, display if links are dead
- image site downloader (for image search engines)
- use of several containers with tor to change IP and retrieve many pages at a time
- wikistat.fr all docs
- etc...
- use of scrapy / selenium
