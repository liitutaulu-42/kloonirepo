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
        return search(koko_tarkistus, kirjoittaja) is not None

    def insert_article(self, kirjoittaja, otsikko, julkaisu, vuosi):
        # artikkelin otsikkoa ja julkaisua ei voi valitoida, koska
        # ne voidaan täyttää vapaassa muodossa. Olisipa kiva, jos sais
        # väärinkirjoitussuojaa...

        assert self.kelpaako_kirjoittaja(kirjoittaja), \
                "Syötetty kirjoittaja oli viallinen"
        assert len(vuosi) == 4 and all(map(str.isdigit, vuosi)), \
                "Syotetty vuosi oli viallinen"

        nimen_alku_sana = match("^[A-Za-z]+", kirjoittaja).group()
        otsikon_alku_sana = match("^[A-Za-z]+", otsikko).group()
        luotu_koodi = f"{nimen_alku_sana}-{otsikon_alku_sana}-{vuosi}"

        artikkeli = Artikkeli(luotu_koodi, kirjoittaja, otsikko, julkaisu, vuosi)
        sql = text(
            "INSERT INTO artikkelit (koodi, kirjoittaja, otsikko, julkaisu, vuosi) "
            "VALUES (:koodi, :kirjoittaja, :otsikko, :julkaisu, :vuosi)"
        )
        self.database.session.execute(sql, artikkeli._asdict())
        self.database.session.commit()

    def get_articles(self):
        sql = text("SELECT * FROM artikkelit")
        content = self.database.session.execute(sql)
        self.database.session.commit()
        return list(map(Artikkeli._make, content))

    def get_bibtex(self):
        content = self.get_articles()
        bibtex_content = ""
        for ref in content:
            ref_bibtex = f"""@article{{{ref.koodi},
    author = {{{ref.kirjoittaja}}},
    title = {{{ref.otsikko}}},
    journal = {{{ref.julkaisu}}},
    year = {ref.vuosi}
}}"""
            bibtex_content += ref_bibtex + "\n\n"
        return bibtex_content
