from flask import render_template, request, redirect  # , jsonify, flash

# from db_helper import reset_db
# from repositories.todo_repository import get_todos, create_todo, set_done
from config import app  # , test_env

# from util import validate_todo
from repositories.reference_repository import Transaction

counter = 0

transaction = Transaction(database=SQLAlchemy(app))

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


# @app.route("/new_todo")
# def new():
#    return render_template("new_todo.html")
#
# @app.route("/create_todo", methods=["POST"])
# def todo_creation():
#    content = request.form.get("content")
#
#    try:
#        validate_todo(content)
#        create_todo(content)
#        return redirect("/")
#    except Exception as error:
#        flash(str(error))
#        return  redirect("/new_todo")
#
# @app.route("/toggle_todo/<todo_id>", methods=["POST"])
# def toggle_todo(todo_id):
#    set_done(todo_id)
#    return redirect("/")
#
# testausta varten oleva reitti
# if test_env:
#    @app.route("/reset_db")
#    def reset_database():
#        reset_db()
#        return jsonify({ 'message': "db reset" })
