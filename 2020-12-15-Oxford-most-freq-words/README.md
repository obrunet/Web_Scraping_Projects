# Web scraping of the most frequent english words


If you're interested in learning new languages, it's important to be able to speak with a good accent, to understand speeches or discussions, read books but also to have enough vocabulary.  
My English is not as fluent as it used to be, but i've decided to work on it. So the question : is how many words in a foreign language you need to know ? Well, [the CEFR English levels](https://en.wikipedia.org/wiki/Common_European_Framework_of_Reference_for_Languages) can provide the beginning of an answer :

| Levels  | Description   | Nb words   | %   |
|---|---|---|---|
|A1| Beginner | 0-2000 | >80% |
|A2| Elementary | 2000-2750 | |
|B1| Intermediate | 2750–3250  | 95% |
|B2| Upper-Intermediate| 3250–3750 | |
|C1| Advanced | 3750–4500 | |
|C2| Proficiency | 4500–5000  | 98% |

*CEFR English levels are used by all modern English language books and English language schools. It is recommended to use CEFR levels in job resumes (curriculum vitae, CV, Europass CV) and other English level references.*

An article from BBC.com intitled "[How many words do you need to speak a language?](https://www.bbc.com/news/world-44569277)" can bring other explanations on the table : 
"*[...] it is incredibly difficult for a language learner to ever know as many words as a native speaker.   
Typically native speakers know 15,000 to 20,000 word families - or lemmas - in their first language.*

*[...] So does someone who can hold a decent conversation in a second language know 15,000 to 20,000 words? Is this a realistic goal for our listener to aim for? Unlikely.*   

*Prof Webb found that people who have been studying languages in a traditional setting - say French in Britain or English in Japan - often struggle to learn more than 2,000 to 3,000 words, even after years of study.*  

*In fact, a study in Taiwan showed that after nine years of learning a foreign language half of the students failed to learn the most frequently-used 1,000 words.*   

*And that is the key, the frequency with which the words you learn appear in day-to-day use in the language you're learning.*   

*You don't need to know all of the words in a language [...]*   

*So which words should we learn? Prof Webb says the most effective way to be able to speak a language quickly is to pick the 800 to 1,000 lemmas which appear most frequently in a language, and learn those.*   

*If you learn only 800 of the most frequently-used lemmas in English, you'll be able to understand 75% of the language as it is spoken in normal life.*"

By searching the web for the most frequently used words, you can quickly arrive on the [OxfordLearnersDictionaries.com](https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000) webpage :

*The Oxford 5000 is an expanded core word list for advanced learners of English. ... the frequency of the words in the Oxford English Corpus, a database of over 2 billion words from different subject areas and contexts which covers British, American and world English.*

... and it could be very interesting to scrape all those words, translate them, and put all of it in an [anki](https://apps.ankiweb.net/) deck to memorize all this good stuff !

# Download the list of all words

First things first, let's grab [the word list of Oxford 3000 and 5000](https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000). This part of the script provides different user agent in order to not get rapidly flagged as a bot, and a function to retrieve a specific web page by its URL with the help of the __requests__ module :


```python
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from random import randint
import time


user_agents = [
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"},
        {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"},
        {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
        {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"},
        {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"},
        {'User-Agent': "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"},
        {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    ]


def retrieve_webpage(req_url):
    """Get a webpage with the requests module & return the response"""
    try:
        req_response = requests.get(req_url, headers=user_agents[randint(0, len(user_agents))])
        req_response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err} for URL {req_url}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err} for URL {req_url}')
        return None
    else:
        # print('Request success!')
        return req_response
    
    
time.sleep(2.4) # in sec
url_wordlist = "https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000"
req_response = retrieve_webpage(url_wordlist)

if not req_response :
    print("fail")
elif str(req_response) == '<Response [200]>':
    print("success")
else:
    print("something wrong")
```

Then, we'll use Beautifulsoup to parse the html page and retrieve the data we need : the word itself, its phonetic pronunciation, its CEFR level, the url of the web page describing each word, the type (verb, noun...) and the american sound (an .mp3 file).  

In order to achieve this goal, it's required to dive deep in the CSS code of the page, to analyze the nested class and their parameters. For instance, in the dev tools of your browser, by clicking on a specific word on the left, you'll see hightlighted the line of the code where the corresponding text can be found.

![Title](./1.png)


```python
s = BeautifulSoup(req_response.content, 'html.parser')
all_elts = s.find_all("li")[34:-44]
words, levels, def_urls, types, sound_urls = [], [], [], [], []

for i in all_elts:
    i = str(i)
    if "data-hw" in i:
        words.append(i.split('data-hw="')[1].split('"')[0])
    else:
        words.append("No word")
    if "data-ox5000" in i:
        levels.append(i.split('data-ox5000="')[1].split('"')[0])
    else:
        levels.append("No level")
    if "href" in i:
        def_urls.append(i.split('href="')[1].split('"')[0])
    else:
        def_urls.append("No def_url")
    if 'class="pos' in i:
        types.append(i.split('class="pos">')[1].split('<')[0])
    else:
        types.append("No types")
    if "data-src-mp3" in i:
        sound_urls.append(i.split('pron-us" data-src-mp3="')[1].split('"')[0])
    else:
        sound_urls.append("No sound url")


df = pd.DataFrame(list(zip(words, levels, def_urls, types, sound_urls)), columns =['words', 'levels', 'def_urls', 'types', 'sound_urls'])
df.to_csv('words_list', index=False)
df.head(3)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>words</th>
      <th>levels</th>
      <th>def_urls</th>
      <th>types</th>
      <th>sound_urls</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>a1</td>
      <td>/definition/english/a_1</td>
      <td>indefinite article</td>
      <td>/media/english/us_pron/a/a__/a__us/a__us_2_rr.mp3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>abandon</td>
      <td>b2</td>
      <td>/definition/english/abandon_1</td>
      <td>verb</td>
      <td>/media/english/us_pron/a/aba/aband/abandon__us...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ability</td>
      <td>a2</td>
      <td>/definition/english/ability_1</td>
      <td>noun</td>
      <td>/media/english/us_pron/a/abi/abili/ability__us...</td>
    </tr>
  </tbody>
</table>
</div>



There isn't any null data in our pandas dataframe, so it seems that we have retrieved all the infos we were looking for...


```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5948 entries, 0 to 5947
    Data columns (total 5 columns):
     #   Column      Non-Null Count  Dtype 
    ---  ------      --------------  ----- 
     0   words       5948 non-null   object
     1   levels      5948 non-null   object
     2   def_urls    5948 non-null   object
     3   types       5948 non-null   object
     4   sound_urls  5948 non-null   object
    dtypes: object(5)
    memory usage: 232.5+ KB
    

Anyway some levels are filled with the default values, but not so many lines are concerned :


```python
df[df['levels'] == 'No level']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>words</th>
      <th>levels</th>
      <th>def_urls</th>
      <th>types</th>
      <th>sound_urls</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>47</th>
      <td>accounting</td>
      <td>No level</td>
      <td>/definition/english/accounting</td>
      <td>noun</td>
      <td>/media/english/us_pron/a/acc/accou/accounting_...</td>
    </tr>
    <tr>
      <th>233</th>
      <td>angrily</td>
      <td>No level</td>
      <td>/definition/english/angrily</td>
      <td>adverb</td>
      <td>/media/english/us_pron/a/ang/angri/angrily__us...</td>
    </tr>
    <tr>
      <th>889</th>
      <td>cleaning</td>
      <td>No level</td>
      <td>/definition/english/cleaning</td>
      <td>noun</td>
      <td>/media/english/us_pron/c/cle/clean/cleaning__u...</td>
    </tr>
    <tr>
      <th>2058</th>
      <td>feeding</td>
      <td>No level</td>
      <td>/definition/english/feeding</td>
      <td>noun</td>
      <td>/media/english/us_pron/f/fee/feedi/feeding__us...</td>
    </tr>
    <tr>
      <th>3176</th>
      <td>major</td>
      <td>No level</td>
      <td>/definition/english/major_2</td>
      <td>noun</td>
      <td>/media/english/us_pron/m/maj/major/major__us_2...</td>
    </tr>
  </tbody>
</table>
</div>



Let's insert the corresponding value :


```python
df.loc[df[df['levels'] == 'No level'].index, 'levels'] = 'a1'
df[df['sound_urls'] == 'No sound url']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>words</th>
      <th>levels</th>
      <th>def_urls</th>
      <th>types</th>
      <th>sound_urls</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3559</th>
      <td>nursing</td>
      <td>b2</td>
      <td>/definition/english/nursing</td>
      <td>noun</td>
      <td>No sound url</td>
    </tr>
  </tbody>
</table>
</div>



Furthermore, there isn't any duplicated line in our dataframe:


```python
df[df.duplicated()].shape[0]
```




    0



# Data cleaning & transformation

We concatenate the relative path with the base url to get the full link. We can also format the level, change a little bit the word type and so on...


```python
BASE_URL = "https://www.oxfordlearnersdictionaries.com"

df['def_urls'] = df['def_urls'].apply(lambda x: BASE_URL + x)
df['levels'] = df['levels'].apply(lambda x: x.upper())
df['types'] = df['types'].apply(lambda x: "(" + x + ")")
df['sound_urls'] = df['sound_urls'].apply(lambda x: BASE_URL + x)
df['sound_files'] = df['sound_urls'].apply(lambda x: x.split("/")[-1])
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>words</th>
      <th>levels</th>
      <th>def_urls</th>
      <th>types</th>
      <th>sound_urls</th>
      <th>sound_files</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>A1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(indefinite article)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>a__us_2_rr.mp3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>abandon</td>
      <td>B2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(verb)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>abandon__us_2.mp3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ability</td>
      <td>A2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(noun)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>ability__us_4.mp3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>able</td>
      <td>A2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(adjective)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>able__us_2.mp3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>abolish</td>
      <td>C1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(verb)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>abolish__us_1.mp3</td>
    </tr>
  </tbody>
</table>
</div>



# Retrieve the sound files

This can be done with a python script or using few shell commands like the ones below:


```python
!mkdir sounds
```


```python
with open("./sounds" + "/" + "url_list.txt", "w") as outfile:
    outfile.write("\n".join(set(df['sound_urls'])))
```


```python
!cd sounds, wget -i url_list.txt
```

# Final step : scraping of all the web pages

Now, we'll loop over the wordlist, and for each element, we use the previous function to retrieve the webpage of the word definition. The beautifulsoup part is more tedious, because it's not so easy to find the relevant infos. Here, several tries and errors are mandatory. Imho, using a jupyternotebook is more convenient.


```python
def get_data(resp):
    """Parse HTTP response of a single webpage with BS4 and return relevant data"""
    soup = BeautifulSoup(resp.content, 'html.parser')
    try:
        phonetic = soup.find_all("div", class_="phons_n_am")[0].find_all("span", class_="phon")[0].contents[0]
    except:
        pass
    try:
        senses = soup.find_all("li", class_="sense")
    except:
        pass
    try:
        definitions = [se.find_all(class_="def")[0].contents[0] for se in senses]
        definitions = [f"{i+1}. {def_.replace(';', ',')}" for i, def_ in enumerate(definitions)]
    except:
        pass
    
    try:
        examples = [] # a list of (list of examples for one definition)
        for se in senses:
            all_examples = se.find_all("ul", class_="examples")[0].find_all(htag="li")
            try:
                all_examples = [e.contents[0].text for e in all_examples]
            except:
                try:
                    all_examples = [ex.find_all(class_="x")[0].text for ex in all_ex]
                except:
                    pass
            examples.append("".join(["<dd>- " + e.replace(';', ',') + "<br>" for e in all_examples ]))
    except:
        pass
    return phonetic, definitions, examples

df_test = df.iloc[:20]
df_test
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>words</th>
      <th>levels</th>
      <th>def_urls</th>
      <th>types</th>
      <th>sound_urls</th>
      <th>sound_files</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>A1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(indefinite article)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>a__us_2_rr.mp3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>abandon</td>
      <td>B2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(verb)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>abandon__us_2.mp3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ability</td>
      <td>A2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(noun)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>ability__us_4.mp3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>able</td>
      <td>A2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(adjective)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>able__us_2.mp3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>abolish</td>
      <td>C1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(verb)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>abolish__us_1.mp3</td>
    </tr>
    <tr>
      <th>5</th>
      <td>abortion</td>
      <td>C1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(noun)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>abortion__us_1.mp3</td>
    </tr>
    <tr>
      <th>6</th>
      <td>about</td>
      <td>A1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(adverb)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>about__us_1.mp3</td>
    </tr>
    <tr>
      <th>7</th>
      <td>about</td>
      <td>A1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(preposition)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>about__us_1.mp3</td>
    </tr>
    <tr>
      <th>8</th>
      <td>above</td>
      <td>A1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(adverb)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>above__us_2.mp3</td>
    </tr>
    <tr>
      <th>9</th>
      <td>above</td>
      <td>A1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(preposition)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>above__us_2.mp3</td>
    </tr>
    <tr>
      <th>10</th>
      <td>abroad</td>
      <td>A2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(adverb)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>abroad__us_4.mp3</td>
    </tr>
    <tr>
      <th>11</th>
      <td>absence</td>
      <td>C1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(noun)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>absence__us_1.mp3</td>
    </tr>
    <tr>
      <th>12</th>
      <td>absent</td>
      <td>C1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(adjective)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>absent__us_1.mp3</td>
    </tr>
    <tr>
      <th>13</th>
      <td>absolute</td>
      <td>B2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(adjective)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>absolute__us_1_rr.mp3</td>
    </tr>
    <tr>
      <th>14</th>
      <td>absolutely</td>
      <td>B1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(adverb)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>absolutely__us_1_rr.mp3</td>
    </tr>
    <tr>
      <th>15</th>
      <td>absorb</td>
      <td>B2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(verb)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>absorb__us_2_rr.mp3</td>
    </tr>
    <tr>
      <th>16</th>
      <td>abstract</td>
      <td>B2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(adjective)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>abstract__us_2_rr.mp3</td>
    </tr>
    <tr>
      <th>17</th>
      <td>absurd</td>
      <td>C1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(adjective)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>absurd__us_1_rr.mp3</td>
    </tr>
    <tr>
      <th>18</th>
      <td>abundance</td>
      <td>C1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(noun)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>abundance__us_1.mp3</td>
    </tr>
    <tr>
      <th>19</th>
      <td>abuse</td>
      <td>C1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(noun)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>abuse__us_3.mp3</td>
    </tr>
  </tbody>
</table>
</div>



this final part will fill in the scraped data into our first dataframe.


```python
for url in df_test["def_urls"].values: #list(df_test["def_urls"]):
    time.sleep(randint(2, 9)) # in sec
    req_response = retrieve_webpage(url.strip())
    if not req_response :
        continue
    elif str(req_response) == '<Response [200]>':
        # success"
        phonetic, definitions, examples = get_data(req_response)
        df_test.loc[df_test[df_test['def_urls'] == url].index, 'phonetic'] = phonetic
        for i, def_ in enumerate(definitions):
            #df_test.loc[df_test['def_urls'] == url][f'definition_{i+1}'] = def_
            df_test.loc[df_test[df_test['def_urls'] == url].index, f'definition_{i+1}'] = def_
        for i, ex in enumerate(examples):
            df_test.loc[df_test[df_test['def_urls'] == url].index, f'examples_{i+1}'] = ex
    else:
        print("something wrong !! for URL {url}")
        
df_test.head()
```

    /opt/anaconda3/lib/python3.8/site-packages/pandas/core/indexing.py:845: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      self.obj[key] = _infer_fill_value(value)
    /opt/anaconda3/lib/python3.8/site-packages/pandas/core/indexing.py:966: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      self.obj[item] = s
    /opt/anaconda3/lib/python3.8/site-packages/pandas/core/indexing.py:671: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      self._setitem_with_indexer(indexer, value)
    <ipython-input-120-fd2d6433854a>:9: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      df_test.loc[df_test[df_test['def_urls'] == url].index, 'phonetic'] = phonetic
    <ipython-input-120-fd2d6433854a>:12: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      df_test.loc[df_test[df_test['def_urls'] == url].index, f'definition_{i+1}'] = def_
    <ipython-input-120-fd2d6433854a>:14: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      df_test.loc[df_test[df_test['def_urls'] == url].index, f'examples_{i+1}'] = ex
    

    Other error occurred: list index out of range for URL https://www.oxfordlearnersdictionaries.com/definition/english/abuse_1
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>words</th>
      <th>levels</th>
      <th>def_urls</th>
      <th>types</th>
      <th>sound_urls</th>
      <th>sound_files</th>
      <th>phonetic</th>
      <th>definition_1</th>
      <th>definition_2</th>
      <th>definition_3</th>
      <th>...</th>
      <th>examples_3</th>
      <th>examples_4</th>
      <th>examples_5</th>
      <th>examples_6</th>
      <th>examples_7</th>
      <th>examples_8</th>
      <th>examples_9</th>
      <th>examples_10</th>
      <th>definition_11</th>
      <th>definition_12</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>A1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(indefinite article)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>a__us_2_rr.mp3</td>
      <td>/ə/</td>
      <td>1. used before countable or singular nouns ref...</td>
      <td>2. used to show that somebody/something is a m...</td>
      <td>3. any, every</td>
      <td>...</td>
      <td>&lt;dd&gt;- A lion is a dangerous animal.&lt;br&gt;</td>
      <td>&lt;dd&gt;- a good knowledge of French&lt;br&gt;&lt;dd&gt;- a sa...</td>
      <td>&lt;dd&gt;- a knife and fork&lt;br&gt;</td>
      <td>&lt;dd&gt;- A thousand people were there.&lt;br&gt;</td>
      <td>&lt;dd&gt;- They cost 50p a kilo.&lt;br&gt;&lt;dd&gt;- I can typ...</td>
      <td>&lt;dd&gt;- She's a little Greta Thunberg.&lt;br&gt;</td>
      <td>&lt;dd&gt;- There's a Mrs Green to see you.&lt;br&gt;</td>
      <td>&lt;dd&gt;- She died on a Tuesday.&lt;br&gt;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>abandon</td>
      <td>B2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(verb)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>abandon__us_2.mp3</td>
      <td>/əˈbændən/</td>
      <td>1. to leave somebody, especially somebody you ...</td>
      <td>2. to leave a thing or place, especially becau...</td>
      <td>3. to stop doing something, especially before ...</td>
      <td>...</td>
      <td>&lt;dd&gt;- They abandoned the match because of rain...</td>
      <td>&lt;dd&gt;- The baby had been abandoned by its mothe...</td>
      <td>&lt;dd&gt;- He abandoned himself to despair.&lt;br&gt;</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ability</td>
      <td>A2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(noun)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>ability__us_4.mp3</td>
      <td>/əˈbɪləti/</td>
      <td>1. the fact that somebody/something is able to...</td>
      <td>2. a level of skill or intelligence</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>able</td>
      <td>A2</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(adjective)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>able__us_2.mp3</td>
      <td>/ˈeɪbl/</td>
      <td>1. to have the skill, intelligence, opportunit...</td>
      <td>2. intelligent, good at something</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>abolish</td>
      <td>C1</td>
      <td>https://www.oxfordlearnersdictionaries.com/def...</td>
      <td>(verb)</td>
      <td>https://www.oxfordlearnersdictionaries.com/med...</td>
      <td>abolish__us_1.mp3</td>
      <td>/əˈbɑːlɪʃ/</td>
      <td>1. to officially end a law, a system or an ins...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 29 columns</p>
</div>



# Conclusion

The final python script and the csv files are available in my Github repository dedicated to scraping stuff.   
This little project is a good example of scraping static webpage. Don't forget that Beautifulsoup is not suited when it comes to deal will pages including embedded javascript. In an other post, i'll share tips and code built upon the selenium package able to translate automatically those words. And finally, i'll show you how to use a csv file to create an anki deck that you can freely use to memorize all this vocabulary.
