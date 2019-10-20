#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os, requests, pickle, html5lib
from bs4 import BeautifulSoup


# In[4]:


url = "https://pokemondb.net/pokedex/ivysaur"


# In[6]:


result = requests.get(url)
if result.status_code != 200:
    print(f'Attempt to retrieve web page failed - result code {result.status_code}')
else:
    soup = BeautifulSoup(result.content, 'html5lib')


# In[64]:


# XPath 
# //*[@id="content"]/div[2]/p/a/img
# soup.select("#content > div:nth-of-type(2) > p > a > img")


# Data

# In[99]:


# species
# also working : soup.find_all('td')[2].string
soup.find("th", text="Species").next_sibling.next_sibling.string


# In[105]:


# height
# working but nonsoup.find_all('td')[3].string.split()[0]
soup.find("th", text="Height").next_sibling.next_sibling.string.split()[0]


# In[106]:


# Weight
soup.find("th", text="Weight").next_sibling.next_sibling.string.split()[0]


# In[113]:


# Abilities
# also working : soup.find_all('td')[5].a 
soup.find("th", text="Abilities").next_sibling.next_sibling.a.text


# Training

# In[116]:


# Catch rate
soup.find("th", text="Catch rate").next_sibling.next_sibling.text.split()[0]


# In[120]:


# Base Friendship
soup.find("th", text="Base")


# In[124]:


# Base Exp.
soup.find("th", text="Base Exp.").next_sibling.next_sibling.text


# In[123]:


# Growth Rate
soup.find("th", text="Growth Rate").next_sibling.next_sibling.text


# Breeding

# In[125]:


# Gender
soup.find("th", text="Gender").next_sibling.next_sibling.text


# Base stats

# In[128]:


# HP
soup.find("th", text="HP").next_sibling.next_sibling.text


# In[129]:


# HP
soup.find("th", text="Attack").next_sibling.next_sibling.text


# In[130]:


# Defense
soup.find("th", text="Defense").next_sibling.next_sibling.text


# In[131]:


# Sp. Atk
soup.find("th", text="Sp. Atk").next_sibling.next_sibling.text


# In[132]:


# Sp. Def
soup.find("th", text="Sp. Def").next_sibling.next_sibling.text


# In[133]:


# Speed
soup.find("th", text="Speed").next_sibling.next_sibling.text


# In[134]:


# Total
soup.find("th", text="Total").next_sibling.next_sibling.text


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[76]:


data = """
<div>
    <label>Name:</label>
    John Smith
</div>
"""

s = BeautifulSoup(data, "html.parser")

label = s.find("label", text="Name:")
print(label.next_sibling.strip())


# In[80]:


print(soup.find(text="Abilities").next_sibling)


# In[112]:


data = """
<div>
    <th>Weight</th>
    <td>tralala</td>
</div>
"""

s = BeautifulSoup(data, "html.parser")

label = s.find("th", text="Weight")
label.next_sibling.next_sibling.string


# In[ ]:





# In[ ]:





# In[ ]:




