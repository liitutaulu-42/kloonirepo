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
    return render_template(
        "index.html", article_content=articles, book_content=books, is_index=True
    )


# lomakkeen lähetä nappi vie .../submit sivulle, josta sovellus hakee tiedot
# ja työntää ne tietokantaan ja lopuksi palauttaa takaisin samalle lomakkeelle
@app.route("/submit/article", methods=["POST"])
def submit_article():
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
    except AssertionError as error:
        flash(str(error))
    return redirect("/form/article")


@app.route("/submit/book", methods=["POST"])
def submit():
    try:
        transaction.insert_book(
            author=request.form.get("author"),
            title=request.form.get("title"),
            year=request.form.get("year"),
            publisher=request.form.get("publisher"),
            address=request.form.get("address"),
        )
        flash("Kirja lisätty onnistuneesti")
    except AssertionError as error:
        flash(str(error))
    return redirect("/form/book")


@app.route("/form/<reference>", methods=["GET"])
# sivu lomakkeille
def form(reference):
    articles = list(transaction.get_articles())
    books = list(transaction.get_books())
    return render_template(
        "form.html",
        form_type=reference,
        article_content=articles,
        book_content=books,
        is_index=False,
    )


@app.route("/submit_delete", methods=["POST"])
# poistaa valitus monivalinta sivulla valitut viitteet
def submit_delete():
    reference_keys = request.form.getlist("selected")
    transaction.delete_references(reference_keys)
    flash("Valitut artikkelit poistettu")
    return redirect("/")


@app.route("/select")
def select():
    return render_template(
        "select_form.html",
        articles=list(transaction.get_articles()),
        books=list(transaction.get_books()),
        is_index=False,
    )


@app.route("/submit_selected", methods=["POST"])
def submit_selected():
    reference_keys = set(request.form.getlist("selected"))
    bibtex_content = transaction.get_bibtex(reference_keys.__contains__)

    response = Response(bibtex_content, mimetype="text/plain")
    response.headers["Content-Disposition"] = 'attachment; filename="viitteet.bib"'
    return response


@app.route("/edit_form")
@app.route("/edit_form/<reference>/<key>")
def edit_form(reference=None, key=None):
    articles = list(transaction.get_articles())
    books = list(transaction.get_books())
    eid = transaction.db_handle.get_id_of(key)
    entry_data = transaction.db_handle.get_fields_of(eid)
    return render_template(
        "edit_form.html",
        key_value=key,
        edit_data=entry_data,
        form_type=reference,
        article_content=articles,
        book_content=books,
        is_index=False,
    )


@app.route("/submit_edit", methods=["POST"])
def submit_edit():
    key = request.form.get("key")
    entry_type = request.form.get("form_type")
    if entry_type == "article":
        try:
            transaction.update_article(
                key=key,
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
        except AssertionError as error:
            flash(str(error))
            return redirect("/")
    if entry_type == "book":
        try:
            transaction.update_book(
                key=key,
                author=request.form.get("author"),
                title=request.form.get("title"),
                year=request.form.get("year"),
                publisher=request.form.get("publisher"),
                address=request.form.get("address"),
            )
        except AssertionError as error:
            flash(str(error))
            return redirect("/")
    flash("Tiedot muutettu onnistuneesti")
    return redirect("/")


@app.route("/bibtex", methods=["GET"])
# lataa bibtex tiedoston
def bibtex():
    bibtex_content = transaction.get_bibtex()

    response = Response(bibtex_content, mimetype="text/plain")
    response.headers["Content-Disposition"] = 'attachment; filename="viitteet.bib"'
    return response


if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
