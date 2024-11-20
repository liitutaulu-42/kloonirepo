from re import search
from sqlalchemy import text

class Transaction:
    def __init__(self, database):
        self.db = database

    def is_author_valid(self, author):
        name = "[A-Za-z]+"
        firstnames = "%s( %s)*" % (name, name)
        first_last = "%s %s" % (firstnames, name)
        comma_separated = "%s(, %s)?, %s" % (name, name, firstnames)
        both_formats = "(%s|%s)" % (first_last, comma_separated)
        all_authors = "^%s( AND %s)*$" % (both_formats, both_formats)
        return search(all_authors, author) != None

    def insert_article(self, key, author, title, journal, year):
        assert self.is_author_valid(author), "Inputted author is invalid"
        values = {"key": key, "author": author, "title": title,
                "journal": journal, "year": year}
        sql = text(
            "INSERT INTO articles (key, author, title, journal, year) "
            "VALUES (:key, :author, :title, :journal, :year)"
        )
        self.db.session.execute(sql, values)
        self.db.session.commit()
