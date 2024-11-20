from sqlalchemy import text

class Transaction:
    def __init__(self, database):
        self.db = database

    def insert_article(self, key, author, title, journal, year):
        values = {"key": key, "author": author, "title": title,
                "journal": journal, "year": year}
        sql = text(
            "INSERT INTO articles (key, author, title, journal, year) "
            "VALUES (:key, :author, :title, :journal, :year)"
        )
        self.db.session.execute(sql, values)
        self.db.session.commit()
