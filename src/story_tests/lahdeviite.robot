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
