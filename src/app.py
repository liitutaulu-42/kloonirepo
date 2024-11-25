from flask import render_template, request, redirect  # , jsonify, flash

from config import app, db  # , test_env

from repositories.reference_repository import Transaction


transaction = Transaction(database=db)

#content = transaction.get_articles()
#parsed_content = []
#for row in content:
#    parsed_content.append((
#        row.koodi,
#        row.kirjoittaja,
#        row.otsikko,
#        row.julkaisu,
#        row.vuosi
#        ))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
# lomakkeen lähetä-nappi vie .../submit sivulle, josta sovellus hakee tiedot
# ja työntää ne tietokantaan ja lopuksi palauttaa sivuston aloitussivulle
def submit_data():
    koodi = request.form.get("koodi")
    kirjoittaja = request.form.get("kirjoittaja")
    otsikko = request.form.get("otsikko")
    julkaisu = request.form.get("julkaisu")
    vuosi = request.form.get("vuosi")

    transaction.insert_article(koodi, kirjoittaja, otsikko, julkaisu, vuosi)
    return redirect("/")
