import urllib.request
import ssl
from flask import request
from application import func   
import pandas as pd

context = ssl._create_unverified_context()


def test_server_running():
    """
    Testar att servern är igång och ger ett svar tillbaka
    """
    assert urllib.request.urlopen("http://127.0.0.1:5000", context=context, timeout=10)


def test_index_page():
    """
    Testar att index-sidan har ett formulär
    """
    url = "http://127.0.0.1:5000"
    with urllib.request.urlopen(url, context=context, timeout=10) as response:
        html = str(response.read())
        assert "</form>" in html


def test_confirm_error_on_get():
    """
    Testar att servern ger felmeddelande när den gör en GET till /resultat
    """
    url = "http://127.0.0.1:5000/resultat"
    with urllib.request.urlopen(url, context=context, timeout=10) as response:
        html = str(response.read())
        assert "finns inte" in html


def test_confirm_error_404():
    """
    Testar att servern ger felmeddelande när den försöker hämta endpoint som inte finns
    """
    url = "http://127.0.0.1:5000/info"
    with urllib.request.urlopen(url, context=context, timeout=10) as response:
        html = str(response.read())
        assert "finns inte" in html


def test_api_response():
    """
    Testar att API:et svarar och ger ett korrekt sökresultat
    """
    url = "https://gutendex.com/books/?languages=en&search=twain"
    with urllib.request.urlopen(url, context=context, timeout=10) as response:
        html = str(response.read())
        assert "twain" in html


def test_func_genre():
    """
    Testar att funktionen genre_api skickar tillbaka en dictionary med genres
    """
    response = func.genre_api()
    assert 'genres' in response


def test_book_api():
    """
    Testar att funktionen book_api skickar tillbaka en Pandas dataframe
    """
    genre = 'drama'
    response = func.book_api(genre)
    assert isinstance(response, pd.DataFrame)
