from flask import Flask, render_template, request
from application import func

app = Flask(__name__)


# Skapar index och hämtar funktion för att hämta alla språkkoder (ISO 639-1)
@app.route('/')
def index():
    sprakkod_data = func.sprakkod('language_code.json')
    genre_data = func.genre_api()
    # Lägger till ett tomt genre fält så det går att söka utan ämne
    genre_data['genres'].append({'id': 00, 'name': ' '})

    # Hämtar en cookie om den finns sparad
    try:
        cookie = request.cookies.get('search')
    except KeyError:
        cookie = ''

    return render_template('index.html', sprakdata=sprakkod_data, genre_data=genre_data, cookie=cookie)


# Skickar POST till /resultat men går man dit utan post så blir det felmeddelande
@app.route('/resultat', methods=['POST'])
def visa_resultat():
    # Felhantering om API för genre inte fungerar
    try:
        # Hämtar genre ur formuläret
        valt_genre = request.form['topic']
    except KeyError:
        # Vid fel blir genre en tom sträng
        valt_genre = ' '

    # Sökfältets innehåll sparas i en cookie-variabel
    try:
        cookie = request.form['search']
    except KeyError:
        cookie = ''

    # Felhantering om book_api ger felaktig information
    try:

        # Hämtar funktionen för book_api och tilldelar till df samt skickar valt_genre-variabel som arg
        df = func.book_api(valt_genre)
        # Skapar en Dataframe i HTML-format
        data_frame = df.to_html(classes="table p-5 table-striped", justify="left")
        # Här skapas ett response objekt och en cookie sätts 
        resp = app.make_response(render_template("resultat.html", data_frame=data_frame))
        resp.set_cookie('search', cookie)
        return resp

    except Exception as e:
        msg = 'Inga böcker hittades'
        return render_template("resultat.html", msg=msg)


@app.errorhandler(404)
def error_not_found(error):
    """
    Felhanterare om användare försöker ansluta till en sida som inte existerar.
    :return: Felmeddelande
    """
    err_msg = 'Sidan du sökte finns inte'
    return render_template('error.html', err_msg=err_msg)


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Felhanterare om användare försöker ansluta till /resultat direkt.
    :return: index.html
    """
    err_msg = 'Sidan du sökte finns inte'
    return render_template('error.html', err_msg=err_msg)
