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
        mock = Mock()
        mock.first.return_value = (1,)
        self.database.session.execute.return_value = mock
        self.transaction.insert_article(
                kirjoittaja="Isaac Newton",
                otsikko="Title of the Article",
                julkaisu="A",
                vuosi="2024",
            )
        self.database.session.execute.assert_called_with(ANY, {
            "id": 1,
            "author": "Isaac Newton",
            "title": "Title of the Article",
            "journal": "A",
            "year": "2024",
        })

    def test_fail_author_syntax(self):
        with self.assertRaises(AssertionError):
            self.transaction.insert_article(
                    kirjoittaja="3",
                    otsikko="Title of the Article",
                    julkaisu="A",
                    vuosi="2024",
                    )

    def test_insert_article_values_same_as_bibtex(self):
        self.database.session.execute.side_effect = [
                ((0, "testi"),),
                (("author", "Kirjoittaja Nimi"),
                 ("journal", "J"),
                 ("title", "Testi Otsikko"),
                 ("year", "2024")),
        ]

        bibtex = self.transaction.get_bibtex()

        expected_bibtex = "@article{testi,\n" \
            "\tauthor = {Kirjoittaja Nimi},\n" \
            "\ttitle = {Testi Otsikko},\n" \
            "\tjournal = {J},\n" \
            "\tyear = 2024\n" \
            "}\n\n"

        self.assertEqual(bibtex, expected_bibtex)
