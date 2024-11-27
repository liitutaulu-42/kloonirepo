from sqlalchemy import text
from config import db, app

TABLE_NAME = "artikkelit"


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


def reset_db():
    print(f"Clearing contents from table {TABLE_NAME}")
    sql = text(f"DELETE FROM {TABLE_NAME}")
    db.session.execute(sql)
    db.session.commit()


def setup_db():
    if table_exists(TABLE_NAME):
        print(f"Table {TABLE_NAME} exists, dropping")
        sql = text(f"DROP TABLE {TABLE_NAME}")
        db.session.execute(sql)
        db.session.commit()

    print(f"Creating table {TABLE_NAME}")
    sql = text(
        f"CREATE TABLE {TABLE_NAME} ("
        "  koodi TEXT PRIMARY KEY,"
        "  kirjoittaja TEXT NOT NULL,"
        "  otsikko TEXT NOT NULL,"
        "  julkaisu TEXT NOT NULL,"
        "  vuosi INT NOT NULL"
        ")"
    )
    db.session.execute(sql)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        setup_db()
