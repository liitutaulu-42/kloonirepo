from re import search
from sqlalchemy import text


class Transaction:
    def __init__(self, database):
        self.db = database

    def is_kirjoittaja_valid(self, kirjoittaja):
        name = "[A-Za-z]+"
        firstnames = "%s( %s)*" % (name, name)
        first_last = "%s %s" % (firstnames, name)
        comma_separated = "%s(, %s)?, %s" % (name, name, firstnames)
        both_formats = "(%s|%s)" % (first_last, comma_separated)
        all_kirjoittajat = "^%s( AND %s)*$" % (both_formats, both_formats)
        return search(all_kirjoittajat, kirjoittaja) != None

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
        self.db.session.execute(sql, values)
        self.db.session.commit()
