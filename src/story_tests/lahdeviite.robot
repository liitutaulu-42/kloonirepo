*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***

Reference management program can be opened
    Go To  ${HOME_URL}
    Title Should Be  Lähdeviiteohjelma
    Page Should Contain  Lähdeviiteohjelma

