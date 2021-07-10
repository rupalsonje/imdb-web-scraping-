# requirements (installation) : pandas library, bs4, requests

import pandas as pd
import requests
from bs4 import BeautifulSoup

movie_name = []
year = []
time = []
rating = []
metascore = []
votes = []
gross = []
type = []
description = []
director = []
cast = []
# below for loop for scraping multiple pages
for i in range(1,1000,100):
    url = f'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start={str(i)}&ref_=adv_nxt'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    movie_data = soup.find_all('div',class_='lister-item mode-advanced')
    for movie in movie_data:
        # movie name
        name = movie.h3.a.text
        movie_name.append(name)
        # year of release
        y = movie.h3.find('span',class_='lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        year.append(y)
        # time of movie
        t = movie.p.find('span',class_='runtime').text
        time.append(t)
        # movie rating
        r = movie.find('div',class_='inline-block ratings-imdb-rating').text.replace('\n','')
        rating.append(r)
        # meta score
        meta = movie.find('span',class_='metascore').text.replace(' ','') if movie.find('span',class_='metascore') else 'NA'
        metascore.append(meta)
        # total votes
        v = movie.find('p',class_='sort-num_votes-visible').find_all('span',attrs={'name':'nv'})
        v1 = v[0].text
        votes.append(v1)
        # gross value
        g = v[1].text if len(v)>1 else 'NA'
        gross.append(g)
        # movie type
        ty = movie.find('span',class_='genre').text.replace(' ','').replace('\n','')
        type.append(ty)
        # movie description
        desc = movie.find_all('p',class_='text-muted')
        description.append(desc[1].text.replace('\n',''))
        # movie director and cast
        d = movie.find('div',class_='lister-item-content').find_all('p')
        di = d[2].find_all('a')
        d1 = di[0].text
        director.append(d1)
        c = ''
        for j in di[1:]:
            c=c[:]+j.text+', '
        cast.append(c)

# converting above list into dataframe
movie_df = pd.DataFrame({'Name of the Movie':movie_name,'Year of release':year,'Watchtime':time,'Movie Rating':rating,'Movie Type':type,'Description':description,'Director':director,'Cast':cast,'Metascore':metascore,'Votes':votes,'Gross Collection':gross})

# exporting dataframe to csv
movie_df.to_csv(r'E:\python1\web scraping\imdb.csv', index = False)