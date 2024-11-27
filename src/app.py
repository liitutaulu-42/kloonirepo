from flask import render_template, request, redirect, flash, jsonify, Response
from db_helper import reset_db
from config import app, db, test_env

from transaction import Transaction


transaction = Transaction(database=db)

@app.route("/", methods=["GET"])
def index():
    articles = transaction.get_articles()
    return render_template("index.html", content=articles)


@app.route("/submit", methods=["POST"])
# lomakkeen lähetä-nappi vie .../submit sivulle, josta sovellus hakee tiedot
# ja työntää ne tietokantaan ja lopuksi palauttaa sivuston aloitussivulle
def submit_data():
    kirjoittaja = request.form.get("kirjoittaja")
    otsikko = request.form.get("otsikko")
    julkaisu = request.form.get("julkaisu")
    vuosi = request.form.get("vuosi")

    try:
        transaction.insert_article(kirjoittaja, otsikko, julkaisu, vuosi)
    except AssertionError as error:
        flash(str(error))
    return redirect("/")


@app.route("/bibtex", methods=["GET"])
# lataa bibtex tiedoston
def bibtex():
    bibtex_content = transaction.get_bibtex()

    response = Response(bibtex_content, mimetype='text/plain')
    response.headers['Content-Disposition'] = 'attachment; filename="viitteet.bib"'
    return response


if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
