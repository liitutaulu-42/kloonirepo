from re import search
from sqlalchemy import text


class Transaction:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def is_kirjoittaja_valid(kirjoittaja):
        name = "[A-Za-z]+"
        firstnames = f"{name}( {name})*"
        first_last = f"{firstnames} {name}"
        comma_separated = f"{name}(, {name})?, {firstnames}"
        both_formats = f"({first_last}|{comma_separated})"
        all_kirjoittajat = f"^{both_formats}( AND {both_formats})*$"
        return search(all_kirjoittajat, kirjoittaja) is not None

    def insert_article(self, koodi, kirjoittaja, otsikko, julkaisu, vuosi):
        assert self.is_kirjoittaja_valid(kirjoittaja), "Inputted kirjoittaja is invalid"
        values = {
            "koodi": koodi,
            "kirjoittaja": kirjoittaja,
            "otsikko": otsikko,
            "julkaisu": julkaisu,
            "vuosi": vuosi,
        }
        sql = text(
            "INSERT INTO artikkelit (koodi, kirjoittaja, otsikko, julkaisu, vuosi) "
            "VALUES (:koodi, :kirjoittaja, :otsikko, :julkaisu, :vuosi)"
        )
        self.database.session.execute(sql, values)
        self.database.session.commit()

    def get_articles(self):
        sql = text("SELECT * FROM artikkelit")
        content = self.database.session.execute(sql)
        self.database.session.commit()
        return content