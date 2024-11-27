from flask import render_template, request, redirect, flash, jsonify, Response
from db_helper import reset_db
from config import app, db, test_env

from repositories.reference_repository import Transaction


transaction = Transaction(database=db)

@app.route("/", methods=["GET"])
def index():
    articles = transaction.get_articles()
    parsed_content = []
    for article in articles:
        parsed_content.append((
            article[0],
            article[1],
            article[2],
            article[3],
            article[4]
            ))
    placeholder_content = [
        ("artikkeli1", "koodi1", "nimi1", "otsikko1", "julkaisu1", "vuosi1"),
        ("artikkeli2", "koodi2", "nimi2", "otsikko2", "julkaisu2", "vuosi2"),
    ]
    return render_template("index.html", content=placeholder_content)


@app.route("/submit", methods=["POST"])
# lomakkeen lähetä-nappi vie .../submit sivulle, josta sovellus hakee tiedot
# ja työntää ne tietokantaan ja lopuksi palauttaa sivuston aloitussivulle
def submit_data():
    koodi = request.form.get("koodi")
    kirjoittaja = request.form.get("kirjoittaja")
    otsikko = request.form.get("otsikko")
    julkaisu = request.form.get("julkaisu")
    vuosi = request.form.get("vuosi")

    try:
        transaction.insert_article(koodi, kirjoittaja, otsikko, julkaisu, vuosi)
    except AssertionError as error:
        flash(str(error))
    return redirect("/")


@app.route("/bibtex", methods=["GET"])
# lataa bibtex tiedoston
def bibtex():
    content = transaction.get_articles()
    bibtex_content = ""
    for ref in content:
        ref_bibtex = f"""@article{{{ref[0]},
    author = {{{ref[1]}}},
    title = {{{ref[2]}}},
    journal = {{{ref[3]}}},
    year = {{{ref[4]}}},
}}"""
        bibtex_content += ref_bibtex + "\n\n"

    response = Response(bibtex_content, mimetype='text/plain')
    response.headers['Content-Disposition'] = 'attachment; filename="viitteet.bib"'
    return response


if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
