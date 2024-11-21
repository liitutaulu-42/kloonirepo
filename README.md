# Lähdeviiteohjelma

[![GHA workflow badge](https://github.com/liitutaulu-42/miniprojekti-liitutaulu-42/workflows/CI/badge.svg)](https://github.com/liitutaulu-42/miniprojekti-liitutaulu-42/actions)

Asiakas määritteet [täältä](https://ohjelmistotuotanto-hy.github.io/speksi/)

Projektin backlog [täältä](https://docs.google.com/spreadsheets/d/1kT_Y4y7KcN3mlNamRc5pwhnNV9R3p1UBAP4W0XShYLs/edit?usp=sharing)

## Ohjelman käynnistys 21.11.2024

- Tee tietokanta oikeilla tauluilla ohjelmaa varten näitä komentoja käyttäen:
- sudo -u postgres psql
- syötä salasanasi
- ALTER USER postgres WITH ENCRYPTED PASSWORD 'postgres';
- CREATE DATABASE postgres;
- GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;
- CREATE TABLE artikkelit (
  koodi TEXT PRIMARY KEY,
  kirjoittaja TEXT NOT NULL,
  otsikko TEXT NOT NULL,
  julkaisu TEXT NOT NULL,
  vuosi INTEGER NOT NULL);
- \q

- Tietokantasi on nyt alustettu ja voit suorittaa ohjelman alla olevilla ohjeilla

Komentorivillä tässä hakemistossa:

- `poetry install`
- `poetry shell`
- `python3 src/index.py`

## Definition of Done

### Sprint 1:

- vaaditut ominaisuudet on toteutettu ja testattu toimiviksi
- ohjelma on asennettavissa ohjeiden avulla
- dokumentaatio on riittävää (README:ssä on ohjeet, linkit backlogiin ja GHA workflowiin)

# Muuta tietoa

Lue flaskistä [täältä](https://ohjelmistotuotanto-hy.github.io/flask/) lisää.

[Tietokanta Sekvenssikaavio](https://sequencediagram.org/index.html#initialData=C4S2BsFMAIBUUsA9gawIYDthugZUigG6QYDOpI6ahISAUHQA5oBOoAxiM1tANIAnAT2DB+AK34NmbEJ27A8SYuHABXUlNYcumBQDFwaUik0y5u6ABE02AEZHIDaHyEjx-ALQA+XEsgr1AC4AQXAkMHUKQlUVHAAiEAwAE0gADwA6AAtgAFtwOIAdDHB+TMREfn4MaDCctBQUSH9DaFBIJKRgQKKACkbBABo0VWBMpBYB0AhIAbEkVRYMNHABwUhWAEoGX2U1Um8DIxRA+HbOmtLy0SroHMQkJJBYorjSVVscsAB9JJs0Ho2cWgpEgLGILCeUAYh2M3msdgcJwQHQU2BUJAwiDQmFu90ezwwcXYLHWwEgXxJADNQSR2JBSACgW1kOgsNiMNDDLCfH4AqRArxVNU2ijoEhqiUymSRIJoGIcGioBhMSJVAMioZsCNVKpoMtwsBIiBotAdSl0SQgA)
