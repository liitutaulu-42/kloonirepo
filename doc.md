## tietokanta taulukot

#### Liitetaulukko esimerkki

| ID | Entry | Key |
| --- | --- | --- |
| 0 | article | A1 |
| 1 | book | B1 |

#### Liitekenttätaulukko esimerkki

| Owner_id | Field | Value |
| --- | --- | --- |
| 0 | author | Isaac Newton |
| 0 | title | Gravity! |
| 0 | journal | Noble's magazine |
| 0 | year | 2024 |
| 1 | ... | ... |

Tämä rajoite on taulukon kentillä: `UNIQUE (Owner_id, Field)`

## Netin sivustot

- `/`: ohjaa muille sivuille
- `/form`: sivu tuetuille liitteiden lomakkeille
  - tuo AssertionError viestin käyttäjälle näkyviin tarvittaessa
- `/submit`: käsittelee lomakkeen tiedot ja lähettää ne tietokantaan
- `/entries`: sivu kaikista liitteistä
- `/delete-form`: liitteistä valitsemis lomake, jossa valitaan poistettavat
- `/submit-delete`: käsittelee poistamislomakkeen

## Lomakkeiden kentät

Kentissä erillinen lomakkeen vinkki suomeksi ja hakunimike englanniksi

#### Artikkelilomakkeen kentät

- pakolliset (lisää "required")
  - piilossa, `reference`, `article`
  - `title`, `otsikko`
  - `author`, `kirjoittaja`
  - `year`, `vuosi`
  - `journal`, `julkaisu`
- vaihtoehtoiset
  - `month`, `kuukausi`
  - `volume`, `vuosikerta`
  - `number`, `julkaisuluku`
  - `pages`,  `sivut`
  - `note`, `lisätiedot`

#### Kirjalomakkeen kentät

- pakolliset (lisää "required")
  - piilossa `reference`, `book`
  - `title`, `otsikko`
  - `author`, `kirjoittaja`
  - `year`, `vuosi`
  - `publisher`, `julkaisija`
  - `address`, `julkaisijan postiosoite`
  
#### Transaction metodit

- `generate_key(title, author, year)`
- `validate_author(author)`
  - heittää AssertionError exceptionin virheestä
- `validate_year(year)`
  - heittää AssertionError exceptionin virheestä
- `insert_article(title, author, year, journal, month="", volume="", number="", pages="", note="")`
  - tarkistaa, että title, author, year ja journal ei ole tyhjä merkkijono
- `insert_book(title, author, year, publisher, address)`
  - tarkistaa, että title, author, year, publisher ja address ei ole tyhjä merkkijono
- `get_articles()` palauttaa listan artikkeleita
- `get_books()` palauttaa listan kirjoja
- `get_bibtex()` palauttaa bibtex -merkkijonon
- `delete_reference(id)` poistaa liitetaulukon id alkion ja liitekenttätaulukon kaikki owner_id arvot

#### Yksikkötestit

- `generate_key` ulostulo on muotoa "nimi-sana-vuosi", jossa nimi on kirjoittajan eka sana ja sana otsiskon eka sana
- `validate_author` sopivalla nimellä ei nouse Exception:iä, väärällä nousee
- `validate_year` sopivalla nimellä ei nouse Exception:iä, väärällä nousee
- `insert_article` database.execute kutsutaan oikeilla arvoilla
- `insert_book` database.execute kutsutaan oikeilla arvoilla
- `get_articles` yhdistää tiedot taulukoista oikein
- `get_books` yhdistää tiedot taulukoista oikein
- `get_bibtex` generoi liitteistä (kokeile erikseen artikkeli ja kirja) ennustettavan ulostulon. assertIn voi käyttää merkkijonojen tutkimiseen
