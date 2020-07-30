import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

headers = {"Accept-Language": "en-US,en;q=0.5"}

titles = []
years = []
ratings = []
time = []
genres = []
imdb_ratings = []
descriptions = []

url = "https://www.imdb.com/search/title/?title_type=tv_series"

results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")

movie_div = soup.find_all('div', class_="lister-item mode-advanced")

for container in movie_div:
    name = container.h3.a.text
    titles.append(name)

    year = container.h3.find('span', class_='lister-item-year').text
    years.append(year)

    rating = container.p.find('span', class_='certificate').text if container.p.find('span', class_='certificate') else '-'
    ratings.append(rating)

    runtime = container.p.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
    time.append(runtime)

    genre = container.p.find('span', class_='genre').text
    genres.append(genre)

    imdb = float(container.strong.text)
    imdb_ratings.append(imdb)

    text_muted = container.find_all('p', class_="text-muted")

    description = text_muted[1].text
    descriptions.append(description)

movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'ratings': ratings,
    'timeMin': time,
    'genres': genres,
    'imdb': imdb_ratings,
    'descriptions': descriptions
})

# Data Cleaning

movies['year'] = movies['year'].map(lambda x: x.lstrip('(').rstrip(')'))

start_year = movies['year'].map(lambda x: x.split("–")[0])
movies["start_year"] = start_year
movies["start_year"] = pd.to_numeric(movies["start_year"], errors='coerce')

end_year = movies['year'].map(lambda x: x.split("–")[1])
movies["end_year"] = end_year
movies["end_year"] = pd.to_numeric(movies["end_year"], errors='coerce', downcast="integer")
movies["end_year"] = movies["end_year"].fillna("-")

del movies['year']

movies['timeMin'] = movies['timeMin'].str.extract('(\d+)')
movies['timeMin'] = pd.to_numeric(movies['timeMin'], errors='coerce')

movies["genres"] = movies["genres"].map(lambda x: x.lstrip('\n'))

movies["descriptions"] = movies["descriptions"].map(lambda x: x.lstrip('\n'))

print(movies, movies.dtypes)
