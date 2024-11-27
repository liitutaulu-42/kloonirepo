*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***
Reference article input form can be opened
    Go To  ${HOME_URL}
    Title Should Be  Lähdeviiteohjelma
    Page Should Contain  Lähdeviiteohjelma

User can input an article with a reference code, author, title, journal, and year
    Go To  ${HOME_URL}
    Input Text  kirjoittaja  Kirjoittaja A
    Input Text  otsikko  Otsikko 1
    Input Text  julkaisu  Julkaisu 1
    Input Text  vuosi  2024
    Click Button  lähetä
    Page Should Contain  Kirjoittaja-Otsikko-2024

User can see a previously input article listed on home page
    Go To  ${HOME_URL}
    Page Should Contain  Kirjoittaja-Otsikko-2024

User sees that an incorrectly input article is not listed
    Go To  ${HOME_URL}
    Input Text  kirjoittaja  Kirjoittaja
    Input Text  otsikko  Otsikko 2
    Input Text  julkaisu  Julkaisu 2
    Input Text  vuosi  2000
    Click Button  lähetä
    Page Should Not Contain  Kirjoittaja-Otsikko-2000

User sees an error message for inputting an incorrectly formatted author
    Go To  ${HOME_URL}
    Input Text  kirjoittaja  Kirjoittaja
    Input Text  otsikko  Otsikko 2
    Input Text  julkaisu  Julkaisu 2
    Input Text  vuosi  2024
    Click Button  lähetä
    Page Should Contain  Syötetty kirjoittaja oli viallinen
    
User sees an error message for inputting an incorrectly formatted year
    Go To  ${HOME_URL}
    Input Text  kirjoittaja  Kirjoittaja B
    Input Text  otsikko  Otsikko 2
    Input Text  julkaisu  Julkaisu 2
    Input Text  vuosi  0.1
    Click Button  lähetä
    Page Should Contain  Syotetty vuosi oli viallinen
