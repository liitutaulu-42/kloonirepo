from flask import render_template, request, redirect  # , jsonify, flash

from config import app, db  # , test_env

from repositories.reference_repository import Transaction

counter = 0

transaction = Transaction(database=db)

@app.route("/")
def index():
    global counter
    counter += 1
    return render_template("index.html", counter=counter)


@app.route("/submit", methods=["POST"])
# lomakkeen lähetä-nappi vie .../submit sivulle, josta sovellus hakee tiedot
# ja työntää ne tietokantaan ja lopuksi palauttaa sivuston aloitussivulle
def submit_data():
    key = request.form.get("key")
    author = request.form.get("author")
    title = request.form.get("title")
    journal = request.form.get("journal")
    year = request.form.get("year")

    transaction.insert_article(key, author, title, journal, year)
    return redirect("/")


