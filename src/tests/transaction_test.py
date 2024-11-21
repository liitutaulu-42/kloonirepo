import unittest

from repositories.reference_repository import Transaction

class SessionStub():
    def __init__(self):
        self.last_insert = tuple()

    def execute(self, _, values):
        self.last_insert = values

    def commit(self):
        pass

class DatabaseStub:
    def __init__(self):
        self.session = SessionStub()

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseStub()
        self.transaction = Transaction(database=self.db)

    def test_initialize_with_no_transactions(self):
        self.assertEqual(self.db.session.last_insert, tuple())

    def test_insert_article_values_are_same(self):
        key = "Doe2023"
        author = "Isaac Newton"
        title = "Title of the Article"
        journal = ""
        year = 2024
        article = {
                "key": key,
                "author": author,
                "title": title,
                "journal": journal,
                "year": year,
        }
        self.transaction.insert_article(key, author, title, journal, year)
        self.assertDictEqual(article, self.db.session.last_insert)

    def test_fail_author_syntax(self):
        with self.assertRaises(AssertionError):
            self.transaction.insert_article(
                    key="Doe2023", 
                    author="3",
                    title="Title of the Article",
                    journal="",
                    year=2024,
                    )

    def test_succeeds_with_author_first_to_last_syntax(self):
        self.transaction.insert_article(
                key="Doe2023", 
                author="Isaac Newton",
                title="Title of the Article",
                journal="",
                year=2024,
                )
