import requests
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd

baseurl = 'https://www.zee5.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991'
}

r = requests.get('https://www.zee5.com/tv-shows/zee-marathi-hd/0-9-zeemarathi')

soup = BeautifulSoup(r.content,'lxml')

productlist = soup.findAll('div',class_="onAirchennelGrid")

productlinks = []

for item in productlist:
    for link in item.find_all('a', href=True):
        productlinks.append(baseurl + link['href'])

# print(len(productlinks))

# testlink = 'https://www.zee5.com/tv-shows/details/abhalmaya/0-6-223'

tv_show_list = []
for link in productlinks:

        r = requests.get(link, headers=headers)

        soup = BeautifulSoup(r.content,'lxml')

        try:
            tv_show_name = soup.find('h1',class_='title').text.strip()
        except:
            tv_show_name = 'NA'

        castName = soup.findAll('div',class_='castName')
        cast_name_list = []
        for cast in castName:
            for cast_item in cast.find_all('h2'):
                cast_name_list.append(cast_item.text.strip())

        seoTable_list = []
        seoTable = soup.findAll('table',class_='movieTable')
        for row in seoTable:
            for item in row.find_all('td'):
                seoTable_list.append(item.text.strip())

        try:
            if seoTable_list[0] == 'Show Released Date':
                release_date = seoTable_list[1]
            elif seoTable_list[2] == 'Show Released Date':
                release_date = seoTable_list[3]
            elif seoTable_list[4] == 'Show Released Date':
                release_date = seoTable_list[5]
        except:
            release_date = 'NA'

        try:
            if seoTable_list[0] == 'Total Episodes':
                total_episodes = seoTable_list[1]
            elif seoTable_list[2] == 'Total Episodes':
                total_episodes = seoTable_list[3]
            elif seoTable_list[4] == 'Total Episodes':
                total_episodes = seoTable_list[5]
        except:
            total_episodes = 'NA'

        try:
            if seoTable_list[0] == 'Genres':
                genres = seoTable_list[1]
            elif seoTable_list[2] == 'Genres':
                genres = seoTable_list[3]
            elif seoTable_list[4] == 'Genres':
                genres = seoTable_list[5]
        except:
            genres = 'NA'

        tv_show = {
            'channel': 'zee_marathi',
            'show_name':tv_show_name,
            'cast_names':cast_name_list,
            'release_date':release_date,
            'total_episodes':total_episodes,
            'genres':genres
        }
        tv_show_list.append(tv_show)
        print('Saving:',tv_show['show_name'])

df = pd.DataFrame(tv_show_list)


df.to_csv('zee_marathi_tv_show.csv', index=False)

print(df.head(3))