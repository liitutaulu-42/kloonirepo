*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***
Reference article input form can be opened
    Go To  ${HOME_URL}
    Title Should Be  Lähdeviiteohjelma
    Page Should Contain  Lähdeviiteohjelma

User can input an atricle with a reference code, author, title, journal, and year
    Go To  ${HOME_URL}
    Input Text  koodi  Koodi1
    Input Text  kirjoittaja  Kirjoittaja A
    Input Text  otsikko  Otsikko1
    Input Text  julkaisu  Julkaisu1
    Input Text  vuosi  2024
    Click Button  lähetä