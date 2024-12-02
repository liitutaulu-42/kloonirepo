from flask import render_template, request, redirect, flash, jsonify, Response
from db_helper import reset_db
from config import app, db, test_env

from transaction import Transaction
from db_handle import DatabaseHandle


transaction = Transaction(DatabaseHandle(database=db))

@app.route("/", methods=["GET"])
def index():
    articles = list(transaction.get_articles())
    return render_template("index.html", content=articles)


@app.route("/submit", methods=["POST"])
# lomakkeen lähetä-nappi vie .../submit sivulle, josta sovellus hakee tiedot
# ja työntää ne tietokantaan ja lopuksi palauttaa sivuston aloitussivulle
def submit_data():
    kirjoittaja = request.form.get("author")
    otsikko = request.form.get("title")
    julkaisu = request.form.get("journal")
    vuosi = request.form.get("year")

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


@app.route("/form", methods=["GET"])
# sivu lomakkeille
def form():
    form_type = request.args.get("type", "article")
    return render_template("form.html", form_type=form_type)

@app.route("/delete-form", methods=["GET"])
# delete-form sivu
def delete_form():
    return render_template("delete-form.html")

if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
