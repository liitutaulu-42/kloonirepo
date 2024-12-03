from flask import render_template, request, redirect, flash, jsonify, Response
from db_helper import reset_db
from config import app, db, test_env

from transaction import Transaction
from db_handle import DatabaseHandle


transaction = Transaction(DatabaseHandle(database=db))


@app.route("/", methods=["GET"])
def index():
    articles = list(transaction.get_articles())
    books = list(transaction.get_books())
    return render_template("index.html", article_content=articles, book_content=books)


@app.route("/submit", methods=["POST"])
# lomakkeen lähetä-nappi vie .../submit sivulle, josta sovellus hakee tiedot
# ja työntää ne tietokantaan ja lopuksi palauttaa sivuston aloitussivulle
def submit_data():
    reference = request.form.get("reference")
    if reference == "article":
        try:
            transaction.insert_article(
                author=request.form.get("author"),
                title=request.form.get("title"),
                journal=request.form.get("journal"),
                year=request.form.get("year"),
                volume=request.form.get("volume"),
                month=request.form.get("month"),
                number=request.form.get("number"),
                pages=request.form.get("pages"),
                note=request.form.get("note"),
            )
            flash("Artikkeli lisätty onnistuneesti")
            return redirect("/")
        except AssertionError as error:
            flash(str(error))
            return redirect("/form?type=article")
    elif reference == "book":
        try:
            transaction.insert_book(
                author=request.form.get("author"),
                title=request.form.get("title"),
                year=request.form.get("year"),
                publisher=request.form.get("publisher"),
                address=request.form.get("address"),
            )
            flash("Kirja lisätty onnistuneesti")
            return redirect("/")
        except AssertionError as error:
            flash(str(error))
            return redirect("/form?type=book")
    return redirect("/")


@app.route("/bibtex", methods=["GET"])
# lataa bibtex tiedoston
def bibtex():
    bibtex_content = transaction.get_bibtex()

    response = Response(bibtex_content, mimetype="text/plain")
    response.headers["Content-Disposition"] = 'attachment; filename="viitteet.bib"'
    return response


@app.route("/form", methods=["GET"])
# sivu lomakkeille
def form():
    form_type = request.args.get("type", "article")
    return render_template("form.html", form_type=form_type)


@app.route("/delete-form", methods=["GET"])
# delete-form sivu
def delete_form():
    articles = list(transaction.get_articles())
    books = list(transaction.get_books())
    return render_template(
        "delete-form.html", article_content=articles, book_content=books
    )


@app.route("/submit-delete", methods=["POST"])
# poista delete-form.html sivulla valitut artikkelit tietokannan tauluista
def submit_delete():
    articles = request.form.getlist("valitut")
    flash(articles)
    return redirect("/")


if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
