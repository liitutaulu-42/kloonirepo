*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***

Reference management program can be opened
    Go To  ${HOME_URL}
    Title Should Be  Lähdeviiteohjelma
    Page Should Contain  Lähdeviiteohjelma

User can open a reference article input form from a menu
    Go To  ${HOME_URL}
    Click Button  Lisää artikkeli
    Page Should Contain  Lisää kirja
    Page Should Contain  Pakolliset kentät

User can open a reference book input form from a menu
    Go To  ${HOME_URL}
    Click Button  Lisää kirja
    Title Should Be  Lisää viite
    Page Should Contain  Lisää kirja
    Page Should Contain  Pakolliset kentät

User can input an article with mandatory fields title, author, journal, and year
    Go To  ${HOME_URL}
    Click Button  Lisää artikkeli
    Input Text  title  Otsikko 1
    Input Text  author  Kirjoittaja A
    Input Text  year  2024
    Input Text  journal  Julkaisu 1
    Click Button  Lähetä
    Page Should Contain  Kirjoittaja-Otsikko-2024

User can see a previously input article listed on home page
    Go To  ${HOME_URL}
    Page Should Contain  Kirjoittaja-Otsikko-2024

User sees that an incorrectly input article is not listed
    Go To  ${HOME_URL}
    Click Button  Lisää artikkeli
    Input Text  title  Otsikko 1
    Input Text  author  Kirjoittaja
    Input Text  year  2024
    Input Text  journal  Julkaisu 1
    Click Button  Lähetä
    Page Should Not Contain  Kirjoittaja-Otsikko-2000

User sees an error message for inputting an incorrectly formatted author
    Go To  ${HOME_URL}
    Click Button  Lisää artikkeli
    Input Text  title  Otsikko 1
    Input Text  author  Kirjoittaja
    Input Text  year  2024
    Input Text  journal  Julkaisu 1
    Click Button  Lähetä
    Page Should Contain  Syötetty kirjoittaja oli viallinen

User sees an error message for inputting an incorrectly formatted year
    Go To  ${HOME_URL}
    Click Button  Lisää artikkeli
    Input Text  title  Otsikko 1
    Input Text  author  Kirjoittaja A
    Input Text  year  0.1
    Input Text  journal  Julkaisu 1
    Click Button  Lähetä
    Page Should Contain  Syötetty vuosi oli viallinen

User sees that an article with missing mandatory fields can not be submitted
    Go To  ${HOME_URL}
    Click Button  Lisää artikkeli
    Page Should Not Contain  Artikkeli lisätty onnistuneesti
    Input Text  title  Otsikko 1
    Click Button  Lähetä
    Page Should Not Contain  Artikkeli lisätty onnistuneesti
    Input Text  author  Kirjoittaja A
    Click Button  Lähetä
    Page Should Not Contain  Artikkeli lisätty onnistuneesti
    Input Text  year  2025
    Click Button  Lähetä
    Page Should Not Contain  Artikkeli lisätty onnistuneesti
    Input Text  journal  Julkaisu 1
    Click Button  Lähetä
    Page Should Contain  Artikkeli lisätty onnistuneesti

User can input an article with optional fields month, volume, number, pages, and note
    Go To  ${HOME_URL}
    Click Button  Lisää artikkeli
    Input Text  title  Otsikko 1
    Input Text  author  Kirjoittaja A
    Input Text  year  2026
    Input Text  journal  Julkaisu 1
    Input Text  month  3
    Input Text  volume  10
    Input Text  number  20
    Input Text  pages  1-2
    Input Text  note  Lisätieto 1
    Click Button  Lähetä
    Page Should Contain  Kirjoittaja-Otsikko-2026
    Page Should Contain  3
    Page Should Contain  10
    Page Should Contain  20
    Page Should Contain  1-2
    Page Should Contain  Lisätieto 1

User can input an book with mandatory fields title, author, year, publisher, and address
    Go To  ${HOME_URL}
    Click Button  Lisää kirja
    Input Text  title  Otsikko 1
    Input Text  author  Kirjoittaja A
    Input Text  year  2000
    Input Text  publisher  Julkaisija 1
    Input Text  address  Osoite 1
    Click Button  Lähetä
    Page Should Contain  Kirjoittaja-Otsikko-2000

User can see a previously input book listed on home page
    Go To  ${HOME_URL}
    Page Should Contain  Kirjoittaja-Otsikko-2000

User sees that a book with missing mandatory fields can not be submitted
    Go To  ${HOME_URL}
    Click Button  Lisää kirja
    Click Button  Lähetä
    Page Should Not Contain  Kirja lisätty onnistuneesti
    Input Text  title  Otsikko 1
    Click Button  Lähetä
    Page Should Not Contain  Kirja lisätty onnistuneesti
    Input Text  author  Kirjoittaja A
    Click Button  Lähetä
    Page Should Not Contain  Kirja lisätty onnistuneesti
    Input Text  year  2001
    Click Button  Lähetä
    Page Should Not Contain  Kirja lisätty onnistuneesti
    Input Text  publisher  Julkaisu 1
    Click Button  Lähetä
    Page Should Not Contain  Kirja lisätty onnistuneesti
    Input Text  address  Osoite 1
    Click Button  Lähetä
    Page Should Contain  Kirja lisätty onnistuneesti

User can navigate to a reference deletion menu
    Go To  ${HOME_URL}
    Click Button  Valitse viitteet
    Page Should Contain  Poista valitut viitteet

User sees a checkbox to delete reference entries on the deletion page
    Go To  ${HOME_URL}
    Click Button  Valitse viitteet
    Page Should Contain Checkbox  name=selected

User can delete reference entries
    Go To  ${HOME_URL}
    Click Button  Valitse viitteet
    Page Should Contain Checkbox  name=selected
    Select Checkbox  Kirjoittaja-Otsikko-2024
    Click Button  Poista valitut viitteet
    Page Should Contain  Valitut artikkelit poistettu

User can select and delete multiple reference entries at once
    Go To  ${HOME_URL}
    Click Button  Valitse viitteet
    Select Checkbox  Kirjoittaja-Otsikko-2025
    Select Checkbox  Kirjoittaja-Otsikko-2026
    Click Button  Poista valitut viitteet
    Page Should Contain  Valitut artikkelit poistettu

User can navigate between program subpages using the top menu buttons
    Go To  ${HOME_URL}
    Page Should Contain  Tervetuloa lähdeviiteohjelmaan
    Click Button  Lisää artikkeli
    Page Should Contain  Lisää artikkeli
    Click Button  Lisää kirja
    Page Should Contain  Lisää kirja
    Click Button  Valitse viitteet
    Page Should Contain Button  Lataa BibTex tiedosto valituista viitteistä
    Page Should Contain Button  Poista valitut viitteet
    Click Button  Etusivulle
    Page Should Contain  Tervetuloa lähdeviiteohjelmaan

User can edit book reference entries
    Go To  ${HOME_URL}
    Click Button  Muokkaa viitettä
    Click Link  Kirja
    Page Should Contain  Muokkaa tietoja
    Input Text  year  2002
    Click Button  Lähetä
    Page Should Contain  Tiedot muutettu onnistuneesti
    Page should Contain  2002

User can edit article reference entries
    Go To  ${HOME_URL}
    Click Button  Lisää artikkeli
    Input Text  title  Otsikko 1
    Input Text  author  Kirjoittaja A
    Input Text  year  2024
    Input Text  journal  Julkaisu 1
    Click Button  Lähetä
    Page Should Contain  Kirjoittaja-Otsikko-2024
    Click Button  Muokkaa viitettä
    Click Link  Artikkeli
    Page Should Contain  Muokkaa tietoja
    Input Text  year  2025
    Click Button  Lähetä
    Page Should Contain  Tiedot muutettu onnistuneesti
    Page should Contain  2025