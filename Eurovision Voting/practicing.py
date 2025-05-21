from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

url = 'https://esc-kompakt.de/eurovision-song-contest-2025-diese-10-acts-haben-sich-aus-dem-zweiten-halbfinale-fuer-das-finale-qualifiziert/'

result = requests.get(url).text
soup = BeautifulSoup(result, 'html.parser')

all_uls = soup.find_all('ul')

# Try to identify the target ul based on its list items' content
target_ul = soup.select_one('.entry-content')

items = [li.text for li in target_ul.find_all('li')]

songs = items[16:42]

laender = []

for i in songs:
    i = i.split(": ")
    laender.append(i)


laender[-1][0] = laender[-1][0].replace("Vereinigtes Königreich", "England")

df = pd.DataFrame(laender)

pd.set_option('display.max_columns', 5)

df[['artist', 'song']] = df[1].str.split(' – ', expand=True)
# df.rename(columns={""})

df = df.drop(1, axis=1)
df = df.rename(columns={0: 'song_country', 'artist': 'song_artist', 'song': 'song_name'})
df_sorted = df.sort_values(by="song_country")


def get_db():
    conn = sqlite3.connect("eurovision.db")
    conn.row_factory = sqlite3.Row
    return conn


df_sorted.to_sql('songs', con=get_db(), if_exists='append', index=False)
