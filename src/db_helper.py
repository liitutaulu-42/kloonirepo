from sqlalchemy import text
from config import db, app

ENTRIES_TABLE = "Entries"
FIELD_TABLE = "Fields"


def table_exists(name):
    sql_table_existence = text(
        "SELECT EXISTS ("
        "  SELECT 1"
        "  FROM information_schema.tables"
        f" WHERE table_name = '{name}'"
        ")"
    )

    result = db.session.execute(sql_table_existence)
    return result.fetchall()[0][0]


def reset_table(name):
    print(f"Clearing contents from table {name}")
    sql = text(f"DELETE FROM {name}")
    db.session.execute(sql)


def reset_db():
    reset_table(ENTRIES_TABLE)
    reset_table(FIELD_TABLE)
    db.session.commit()

def drop_last_session_table(name):
    if table_exists(name):
        print(f"Table {name} exists, dropping")
        sql = text(f"DROP TABLE {name}")
        db.session.execute(sql)
        db.session.commit()

def setup_db():
    drop_last_session_table(ENTRIES_TABLE)
    drop_last_session_table(FIELD_TABLE)

    print("Creating entry enum type")
    sql = text("CREATE TYPE entry_t AS ENUM ('article', 'book');")
    db.session.execute(sql)
    db.session.commit()

    # Verrataan:
    # SELECT * FROM Entries WHERE entry = 'article';

    print("Creating field enum type")
    sql = text(
        "CREATE TYPE field_t AS ENUM ("
        "  'author', 'title', 'journal',"
        "  'year', 'volume', 'number',"
        "  'pages', 'month', 'note',"
        "  'publisher', 'address'"
        ");"
    )
    db.session.execute(sql)
    db.session.commit()

    print(f"Creating table {ENTRIES_TABLE}")
    sql = text(
        f"CREATE TABLE {ENTRIES_TABLE} ("
        "  id serial PRIMARY KEY,"
        "  entry entry_t,"
        "  key text UNIQUE"
        ");"
    )
    db.session.execute(sql)
    db.session.commit()

    print(f"Creating table {FIELD_TABLE}")
    sql = text(
        f"CREATE TABLE {FIELD_TABLE} ("
        f" owner_id serial REFERENCES {ENTRIES_TABLE}(id),"
        "  field field_t,"
        "  value text,"
        "  UNIQUE (owner_id, field)"
        ");"
    )
    db.session.execute(sql)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        setup_db()
