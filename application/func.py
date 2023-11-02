import json
import requests
from flask import request
import pandas as pd
import urllib.request
import ssl


# Läser arg (i vårat fall language_code.json) så som vi lärt oss i programmering 1
def sprakkod(filnamn):
    """
    Läser in en fil i json-format.
    return: Dictionary
    """
    try:
        with open(filnamn, 'r') as fil:
            data_dictionary = json.load(fil)
        return data_dictionary

    # Returnerar tom lista ifall filnamnet saknas
    except FileNotFoundError:
        return {}


def genre_api():
    """
    Hämtar genres från filmer från https://api.themoviedb.org/3/genre/movie/list?language=en
    Return: Dictionary i JSON format
    """

    # API
    url_genre_movie = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    # API-token
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMDQxM2VkYmIzYzJkZmRjNDhlZTYwMTI1MmE5MTAyYyIsInN1YiI6IjY1M2I3YTdkNzE5YWViMDBlMTE5MDBhMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.U7y8z2MlqaLM5-AquU2nYecH2KDI_ZJp7b0wDiavbcw"
    }

    # Hämtar resultat
    response = requests.get(url_genre_movie, headers=headers)
    if response.status_code == 200:
        # Returnerar dictionary (json) vid statuskod 200
        return response.json()
    else:
        # Om servern ger en felkod returneras en tom dictionary
        return {}


def book_api(valt_genre):
    """
    Hämtar API-information från https://gutendex.com/books/? 
    Skriver ut Title, Authors, Subjects samt Languages

    return: Pandas Dataframe
    """
    # Tilldelar det man väljer i form till valt_languages och valt_search.
    # Felhantering om vissa fält inte är ifyllda
    try:
        valt_languages = request.form['languages']
    except Exception:
        valt_languages = 'en'
    
    try:
        valt_search = request.form['search']
    except Exception:
        valt_search = ''

    # URL så som API är uppbyggd (valt_genre hämtas från en dropdown från annan API, hämtar med arg)
    url_books = f"https://gutendex.com/books/?languages={valt_languages}&search={valt_search}&topic={valt_genre}"
    context = ssl._create_unverified_context()

    # Felhantering om API returnerar felaktig data eller inte svarar.
    try:
        # Data hämtas från URL:en.
        json_data = urllib.request.urlopen(url_books, context=context).read()

        # Gör om från JSON format till en lista med dictionarys.
        result_data = json.loads(json_data)
        # En dataframe skapas utifrån sökresultatet
        df = pd.DataFrame(result_data['results'])

        # Väljer ut de kolumner som vi vill presentera
        df = df[['title', 'authors', 'subjects', 'languages']]

        # Omvandlar listor till strängar för att göra det mer läsbart
        # https://stackoverflow.com/questions/45306988/column-of-lists-convert-list-to-string-as-a-new-column
        # svaret som funka: https://stackoverflow.com/a/60416031
        df['authors'] = df['authors'].apply(lambda authors: ', '.join([author['name'] for author in authors]))
        df['subjects'] = df['subjects'].apply(lambda subjects: ', '.join(subjects))
        df['languages'] = df['languages'].apply(lambda languages: ', '.join(languages))

        # Byter namn på kolumnerna så det ser bättre ut
        df.rename(columns={'title': 'Title', 'authors': 'Author', 'subjects': 'Subjects', 'languages': 'Languages'},
                  inplace=True)
        return df

    except Exception as error:
        return df, error
