# Lähdeviiteohjelma

[![GHA workflow badge](https://github.com/liitutaulu-42/miniprojekti-liitutaulu-42/workflows/CI/badge.svg)](https://github.com/liitutaulu-42/miniprojekti-liitutaulu-42/actions)

Asiakas määritteet [täältä](https://ohjelmistotuotanto-hy.github.io/speksi/)

Projektin backlog [täältä](https://docs.google.com/spreadsheets/d/1kT_Y4y7KcN3mlNamRc5pwhnNV9R3p1UBAP4W0XShYLs/edit?usp=sharing)

## Ohjelman käynnistys 21.11.2024

- Tee tietokanta oikeilla tauluilla ohjelmaa varten näitä komentoja käyttäen:
- `sudo -u postgres psql`
- syötä salasanasi
- `ALTER USER postgres WITH ENCRYPTED PASSWORD 'postgres';`
- `CREATE DATABASE postgres;`
- `GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;`
- `CREATE TABLE artikkelit (
  koodi TEXT PRIMARY KEY,
  kirjoittaja TEXT NOT NULL,
  otsikko TEXT NOT NULL,
  julkaisu TEXT NOT NULL,
  vuosi INTEGER NOT NULL);`
- `\q`

- Tietokantasi on nyt alustettu ja voit käyttää ohjelmaa alla olevilla ohjeilla
  
## Käyttöohjeet 21.11.2024
Komentorivillä tässä hakemistossa:

- `poetry install`
- `poetry shell`
- `python3 src/index.py`
- avaa sovellus [tästä](http://localhost:5001/)
- kentät ovat muuten vapaita muotoilultaan, mutta kirjoittajatieto tulee merkitä pelkästään a-z/A-Z merkeillä ja vähintään yhdellä välilyönnillä ja vuosi pitää ilmoittaa kokonaislukuna

## Definition of Done

### Koodin laatu
- koodin pitäisi olla sellaista että sitä ei tarvitse enää muuttaa kyseisestä sprinttiä varten
- koodi pitäisi olla pylintin mukaista
- kaikki koodille tehdyt testit pitää mennä läpi
- vaikeissa tapauksissa koodi selitetään kommenteilla, mutta koodin pitäisi olla helppolukuista
- muuttujat ja nimet suomeksi

### Tehtävänhallinta
- taskit ovat tunnistettavia nimeltä (kirjain + luku) mm. issuesseissa

## Muuta tietoa

Lue flaskistä [täältä](https://ohjelmistotuotanto-hy.github.io/flask/) lisää.

[Tietokanta Sekvenssikaavio](https://sequencediagram.org/index.html#initialData=C4S2BsFMAIBUUsA9gawIYDthugZUigG6QYDOpI6ahISAUHQA5oBOoAxiM1tANIAnAT2DB+AK34NmbEJ27A8SYuHABXUlNYcumBQDFwaUik0y5u6ABE02AEZHIDaHyEjx-ALQA+XEsgr1AC4AQXAkMHUKQlUVHAAiEAwAE0gADwA6AAtgAFtwOIAdDHB+TMREfn4MaDCctBQUSH9DaFBIJKRgQKKACkbBABo0VWBMpBYB0AhIAbEkVRYMNHABwUhWAEoGX2U1Um8DIxRA+HbOmtLy0SroHMQkJJBYorjSVVscsAB9JJs0Ho2cWgpEgLGILCeUAYh2M3msdgcJwQHQU2BUJAwiDQmFu90ezwwcXYLHWwEgXxJADNQSR2JBSACgW1kOgsNiMNDDLCfH4AqRArxVNU2ijoEhqiUymSRIJoGIcGioBhMSJVAMioZsCNVKpoMtwsBIiBotAdSl0SQgA)
