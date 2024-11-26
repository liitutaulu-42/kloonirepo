from re import search
from sqlalchemy import text


class Transaction:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def is_kirjoittaja_valid(kirjoittaja):
        # Kirjoittajakentällä on esitysmuodot:
        # 1. {Etunimet Sukunimi}
        # 2. {Sukunimi, Etunimet}
        # 3. {Sukunimi, Liite, Etunimet}
        # tai kun on monta kirjoittajaa: kirjoittaja AND kirjoittaja

        # Koodi käyttää regexiä ja formaattimerkkijonoja lomitusten, joka
        # vaikeuttaa koodin lukua, mutta parantaa sen ajattelua.

        # nimi esitetään aakkosisena merkkijonona, koska en löytänyt toista
        # ohjeistusta
        name = "[A-Za-z]+"
        # tosiaan montaa etunimeä tuetaan ja se vaikutti olevan ainoastaan
        # etunimet väleillä erotettuina
        firstnames = f"{name}( {name})*"
        # tämä käsittelee 1. esitysmuodon
        first_last = f"{firstnames} {name}"
        # tämä loput eli 2. ja 3. esitysmuodot.
        # liite esiintyy välillä, niin se on helppo kuvata regexillä
        comma_separated = f"{name}(, {name})?, {firstnames}"
        # sitten yhdistetään esiintymismuodot
        both_formats = f"({first_last}|{comma_separated})"
        # lopuksi tarkistamme, että koko merkkijono tottelee
        # yksittäisen tai monen kirjoittajan syotettä.
        all_kirjoittajat = f"^{both_formats}( AND {both_formats})*$"
        return search(all_kirjoittajat, kirjoittaja) is not None

    def insert_article(self, koodi, kirjoittaja, otsikko, julkaisu, vuosi):
        # artikkelin otsikkoa ja julkaisua ei voi valitoida, koska
        # ne voidaan täyttää vapaassa muodossa. Olisipa kiva, jos sais
        # väärinkirjoitussuojaa...

        assert self.is_kirjoittaja_valid(kirjoittaja), \
                "Syötetty kirjoittaja oli viallinen"
        assert len(vuosi) == 4 and all(map(str.isdigit, vuosi)), \
                "Syotetty vuosi oli viallinen"

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
