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
        self.database = DatabaseStub()
        self.transaction = Transaction(database=self.database)

    def test_initialize_with_no_transactions(self):
        self.assertEqual(self.database.session.last_insert, tuple())

    def test_insert_article_values_are_same(self):
        koodi = "Doe2023"
        kirjoittaja = "Isaac Newton"
        otsikko = "Title of the Article"
        julkaisu = ""
        vuosi = 2024
        self.transaction.insert_article(koodi, kirjoittaja, otsikko, julkaisu, vuosi)
        last_insert = self.database.session.last_insert
        self.assertEqual(last_insert["koodi"], koodi)
        self.assertEqual(last_insert["kirjoittaja"], kirjoittaja)
        self.assertEqual(last_insert["otsikko"], otsikko)
        self.assertEqual(last_insert["julkaisu"], julkaisu)
        self.assertEqual(last_insert["vuosi"], vuosi)

    def test_fail_author_syntax(self):
        with self.assertRaises(AssertionError):
            self.transaction.insert_article(
                    koodi="Doe2023",
                    kirjoittaja="3",
                    otsikko="Title of the Article",
                    julkaisu="",
                    vuosi=2024,
                    )

    def test_succeeds_with_author_first_to_last_syntax(self):
        self.transaction.insert_article(
                koodi="Doe2023",
                kirjoittaja="Isaac Newton",
                otsikko="Title of the Article",
                julkaisu="",
                vuosi=2024,
                )
