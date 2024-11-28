from collections import namedtuple
from re import search, match
from sqlalchemy import text

Artikkeli = namedtuple("Artikkeli",
        ["koodi", "kirjoittaja", "otsikko", "julkaisu", "vuosi"])

class Transaction:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def kelpaako_kirjoittaja(kirjoittaja):
        # Kirjoittajakentällä on esitysmuodot:
        # 1. {Etunimet Sukunimi}
        # 2. {Sukunimi, Etunimet}
        # 3. {Sukunimi, Liite, Etunimet}
        # tai kun on monta kirjoittajaa: kirjoittaja AND kirjoittaja

        # Koodi käyttää regexiä ja formaattimerkkijonoja lomitusten, joka
        # vaikeuttaa koodin lukua, mutta parantaa sen ajattelua.

        # nimi esitetään aakkosisena merkkijonona, koska en löytänyt toista
        # ohjeistusta
        nimi = "[A-Za-z]+"
        # tosiaan montaa etunimeä tuetaan ja se vaikutti olevan ainoastaan
        # etunimet väleillä erotettuina
        etunimet = f"{nimi}( {nimi})*"
        # tämä käsittelee 1. esitysmuodon
        etunimet_sukunimi = f"{etunimet} {nimi}"
        # tämä loput eli 2. ja 3. esitysmuodot.
        # liite esiintyy välillä, niin se on helppo kuvata regexillä
        pilkulla_jaetut = f"{nimi}(, {nimi})?, {etunimet}"
        # sitten yhdistetään esiintymismuodot
        molemmat_saannot = f"({etunimet_sukunimi}|{pilkulla_jaetut})"
        # lopuksi tarkistamme, että koko merkkijono tottelee
        # yksittäisen tai monen kirjoittajan syotettä.
        koko_tarkistus = f"^{molemmat_saannot}( AND {molemmat_saannot})*$"
        assert search(koko_tarkistus, kirjoittaja) is not None, \
                "Syötetty kirjoittaja oli viallinen"


    def insert_article(self, kirjoittaja, otsikko, julkaisu, vuosi):
        self.kelpaako_kirjoittaja(kirjoittaja)
        assert len(vuosi) == 4 and all(map(str.isdigit, vuosi)), \
                "Syotetty vuosi oli viallinen"

        nimen_alku_sana = match("^[A-Za-z]+", kirjoittaja).group()
        otsikon_alku_sana = match("^[A-Za-z]+", otsikko).group()
        genkey = f"{nimen_alku_sana}-{otsikon_alku_sana}-{vuosi}"

        sql = text(
            "INSERT INTO Entries (entry, key)"
            "VALUES ('article', :id)"
            "RETURNING id;"
        )
        eid = self.database.session.execute(sql, {"id": genkey}).first()[0]

        sql = text(
            "INSERT INTO Fields (owner_id, field, value) VALUES"
            "  (:id, 'author', :author),"
            "  (:id, 'title', :title),"
            "  (:id, 'journal', :journal),"
            "  (:id, 'year', :year);"
        )
        self.database.session.execute(sql, {
            "id": eid,
            "author": kirjoittaja,
            "title": otsikko,
            "journal": julkaisu,
            "year": vuosi,
        })
        self.database.session.commit()

    def get_articles(self):
        ret = []
        sql = text(
            "SELECT id, key "
            "FROM Entries "
            "WHERE entry='article' "
        )
        for eid, key in self.database.session.execute(sql):
            sql = text(
                "SELECT value "
                "FROM Fields "
                "WHERE owner_id=:id "
                "ORDER BY field "
            )
            fields = self.database.session.execute(sql, {"id": eid})
            author, journal, title, year = tuple(field[0] for field in fields)
            ret.append(Artikkeli(key, author, title, journal, year))

        return ret

    def get_bibtex(self):
        content = self.get_articles()
        bibtex_content = ""
        for ref in content:
            ref_bibtex = f"@article{{{ref.koodi},\n" \
                f"\tauthor = {{{ref.kirjoittaja}}},\n" \
                f"\ttitle = {{{ref.otsikko}}},\n" \
                f"\tjournal = {{{ref.julkaisu}}},\n" \
                f"\tyear = {ref.vuosi}\n" \
                "}"
            bibtex_content += ref_bibtex + "\n\n"
        return bibtex_content
