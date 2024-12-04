*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***

Reference management program can be opened
    Go To  ${HOME_URL}
    Title Should Be  Lähdeviiteohjelma
    Page Should Contain  Lähdeviiteohjelma

User can open a reference article input form from a dropdown menu
    Go To  ${HOME_URL}
    Page Should Contain  Lisää uusi viite
    Select From List By Value	type	article
    Click Button  Siirry lomakkeelle
    Page Should Contain  Lisää artikkeli

User can open a reference book input form from a dropdown menu
    Go To  ${HOME_URL}
    Page Should Contain  Lisää uusi viite
    Select From List By Value	type	book
    Click Button  Siirry lomakkeelle
    Page Should Contain  Lisää kirja

User can input an article with mandatory fields title, author, journal, and year
    Go To  ${HOME_URL}
    Select From List By Value	type	article
    Click Button  Siirry lomakkeelle
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
    Select From List By Value	type	article
    Click Button  Siirry lomakkeelle
    Input Text  title  Otsikko 1
    Input Text  author  Kirjoittaja
    Input Text  year  2024
    Input Text  journal  Julkaisu 1
    Click Button  Lähetä
    Page Should Not Contain  Kirjoittaja-Otsikko-2000

User sees an error message for inputting an incorrectly formatted author
    Go To  ${HOME_URL}
    Select From List By Value	type	article
    Click Button  Siirry lomakkeelle
    Input Text  title  Otsikko 1
    Input Text  author  Kirjoittaja
    Input Text  year  2024
    Input Text  journal  Julkaisu 1
    Click Button  Lähetä
    Page Should Contain  Syötetty kirjoittaja oli viallinen

User sees an error message for inputting an incorrectly formatted year
    Go To  ${HOME_URL}
    Select From List By Value	type	article
    Click Button  Siirry lomakkeelle
    Input Text  title  Otsikko 1
    Input Text  author  Kirjoittaja A
    Input Text  year  0.1
    Input Text  journal  Julkaisu 1
    Click Button  Lähetä
    Page Should Contain  Syötetty vuosi oli viallinen

User sees that an article with missing mandatory fields can not be submitted
    Go To  ${HOME_URL}
    Select From List By Value	type	article
    Click Button  Siirry lomakkeelle
    Click Button  Lähetä
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

User can input an book with mandatory fields title, author, year, publisher, and address
    Go To  ${HOME_URL}
    Select From List By Value	type	book
    Click Button  Siirry lomakkeelle
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
    Select From List By Value	type	book
    Click Button  Siirry lomakkeelle
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
    Click Button  Poista liitteitä
    Page Should Contain  Poista liitteitä

User can navigate back to the main page from the reference deletion menu
    Go To  ${HOME_URL}
    Click Button  Poista liitteitä
    Click Link  link=Takaisin etusivulle
    Page Should Contain  Lähdeviiteohjelma

User sees a checkbox to delete reference entries on the deletion page
    Go To  ${HOME_URL}
    Click Button  Poista liitteitä
    Page Should Contain Checkbox  name=valitut