import unittest
from unittest.mock import Mock, ANY

from transaction import Transaction

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.database = Mock()
        self.transaction = Transaction(database=self.database)

    def test_initialize_with_no_transactions(self):
        self.database.session.commit.assert_not_called()

    def test_insert_article_values_are_same(self):
        self.transaction.insert_article(
                kirjoittaja="Isaac Newton",
                otsikko="Title of the Article",
                julkaisu="",
                vuosi="2024",
            )
        self.database.session.execute.assert_called_once_with(ANY, {
            "koodi": ANY,
            "kirjoittaja": "Isaac Newton",
            "otsikko": "Title of the Article",
            "julkaisu": "",
            "vuosi": "2024",
            })

    def test_fail_author_syntax(self):
        with self.assertRaises(AssertionError):
            self.transaction.insert_article(
                    kirjoittaja="3",
                    otsikko="Title of the Article",
                    julkaisu="",
                    vuosi="2024",
                    )
