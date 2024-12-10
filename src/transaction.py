from re import search, match


class Transaction:
    def __init__(self, db_handle):
        self.db_handle = db_handle

    @staticmethod
    def validate_author(author):
        # Kirjoittajakentällä on esitysmuodot:
        # 1. {Etunimet Sukunimi}
        # 2. {Sukunimi, Etunimet}
        # 3. {Sukunimi, Liite, Etunimet}
        # tai kun on monta kirjoittajaa: kirjoittaja AND kirjoittaja

        # Koodi käyttää regexiä ja formaattimerkkijonoja lomitusten, joka
        # vaikeuttaa koodin lukua, mutta parantaa sen ajattelua.

        # nimi esitetään aakkosisena merkkijonona, koska en löytänyt toista
        # ohjeistusta
        name = r"\w+"
        # tosiaan montaa etunimeä tuetaan ja se vaikutti olevan ainoastaan
        # etunimet väleillä erotettuina
        first_names = f"{name}( {name})*"
        # tämä käsittelee 1. esitysmuodon
        firsts_last = f"{first_names} {name}"
        # tämä loput eli 2. ja 3. esitysmuodot.
        # liite esiintyy välillä, niin se on helppo kuvata regexillä
        comma_separated = f"{name}(, {name})?, {first_names}"
        # sitten yhdistetään esiintymismuodot
        both_patterns = f"({firsts_last}|{comma_separated})"
        # lopuksi tarkistamme, että koko merkkijono tottelee
        # yksittäisen tai monen kirjoittajan syotettä.
        whole_match = f"^{both_patterns}( AND {both_patterns})*$"
        assert (
            search(whole_match, author) is not None
        ), "Syötetty kirjoittaja oli viallinen"

    @staticmethod
    def validate_year(year):
        assert len(year) == 4 and all(
            map(str.isdigit, year)
        ), "Syötetty vuosi oli viallinen"

    @staticmethod
    def generate_key(author, title, year):
        name_start = match(r"\w+", author).group()
        title_start = match(r"\w+", title).group()
        return f"{name_start}-{title_start}-{year}"

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def insert_article(
        self,
        author,
        title,
        journal,
        year,
        month="",
        volume="",
        number="",
        pages="",
        note="",
    ):
        self.validate_author(author)
        self.validate_year(year)

        # tähän valinnaiset; tarkista ennen, että kuitenkin täytetty

        genkey = self.generate_key(author, title, year)

        eid = self.db_handle.create_entry("article", genkey)

        self.db_handle.add_field(eid, "author", author)
        self.db_handle.add_field(eid, "title", title)
        self.db_handle.add_field(eid, "journal", journal)
        self.db_handle.add_field(eid, "year", year)
        if month != "":
            self.db_handle.add_field(eid, "month", month)
        if volume != "":
            self.db_handle.add_field(eid, "volume", volume)
        if number != "":
            self.db_handle.add_field(eid, "number", number)
        if pages != "":
            self.db_handle.add_field(eid, "pages", pages)
        if note != "":
            self.db_handle.add_field(eid, "note", note)

        self.db_handle.commit()

    def get_articles(self):
        for eid, key in self.db_handle.get_references("article"):
            article_fields = self.db_handle.get_fields_of(eid)
            author = article_fields["author"]
            journal = article_fields["journal"]
            title = article_fields["title"]
            year = article_fields["year"]
            month = article_fields.get("month", "-")
            volume = article_fields.get("volume", "-")
            number = article_fields.get("number", "-")
            pages = article_fields.get("pages", "-")
            note = article_fields.get("note", "-")
            yield (
                key,
                author,
                title,
                journal,
                year,
                month,
                volume,
                number,
                pages,
                note,
            )

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def insert_book(self, author, title, year, publisher, address):
        genkey = self.generate_key(author, title, year)
        entry_id = self.db_handle.create_entry("book", genkey)

        self.validate_author(author)
        self.validate_year(year)

        self.db_handle.add_field(entry_id, "author", author)
        self.db_handle.add_field(entry_id, "title", title)
        self.db_handle.add_field(entry_id, "year", year)
        self.db_handle.add_field(entry_id, "publisher", publisher)
        self.db_handle.add_field(entry_id, "address", address)

        self.db_handle.commit()

    def get_books(self):
        for eid, key in self.db_handle.get_references("book"):
            book_fields = self.db_handle.get_fields_of(eid)
            author = book_fields["author"]
            title = book_fields["title"]
            year = book_fields["year"]
            publisher = book_fields["publisher"]
            address = book_fields["address"]

            yield key, author, title, year, publisher, address

    def delete_references(self, reference_keys):
        for key in reference_keys:
            eid = self.db_handle.get_id_of(key)
            self.db_handle.delete_fields_of(eid)
            self.db_handle.delete_entry(eid)
        self.db_handle.commit()

    def get_bibtex(self):
        bibtex_content = ""
        for key, author, title, journal, year, _, _, _, _, _ in self.get_articles():
            ref_bibtex = (
                f"@article{{{key},\n"
                f"\tauthor = {{{author}}},\n"
                f"\ttitle = {{{title}}},\n"
                f"\tjournal = {{{journal}}},\n"
                f"\tyear = {year}\n"
                "}"
            )
            bibtex_content += ref_bibtex + "\n\n"
        return bibtex_content
