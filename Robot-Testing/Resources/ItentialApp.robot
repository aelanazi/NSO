*** Settings ***
Documentation     Itential LGI R&D Lab (Browser Test)
Library           SeleniumLibrary
Library           String
Library           Collections

*** Variables ***
${HOST}           http://172.30.150.116:3000/login
${HOST-PROD}      https://172.23.29.210:3443/login
${user-prod}      aelanazi
${passwd-prod}    xxx
${user-lab}       corpuser1
${passwd-lab}     cisco123
${chrome}         chrome
${internetexplorer}    ie
@{FORM-DATA-E-LINE-EPL}    CUST1    SR-NL-991    lg-ciena-3916-A    110000101    89    3    2
...               1    100000    BE    None

*** Keywords ***
Begin Test With Chrome
    Open Browser    about:blank    ${chrome}

Begin Test With IE
    Open Browser    about:blank    ${internetexplorer}

Go To PH Login
    Go To    ${HOST}

Input Username And Password PH Login Page
    Input Text    xpath://*[@id="input_username"]/input    ${user-lab}
    Input Password    xpath://*[@id="input_password"]/input    ${passwd-lab}
    Click Button    id=sign_in
    sleep    2s

Navigate To Service Catalog Page
    Go To    http://172.30.150.116:3000/service_catalog/
    #Click Button    xpath://*[@id="app-list"]/li[10]/button
    sleep    2s

Navigate To E-Line EPL Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[9]/td[3]/button
    sleep    2s

Populate E-Line EPL Forum With Service Parameters
    Input Text    xpath://*[@id="id_354c7ebb-da8f-4267-b3aa-9b220581134b"]    @{FORM-DATA-E-LINE-EPL}[0]
    Input Text    xpath://*[@id="id_95a36447-bf81-4ad5-a0c3-0a98c22555e2"]    @{FORM-DATA-E-LINE-EPL}[1]
    Input Text    xpath://*[@id="id_5e5d9068-479f-4d02-b1d1-3a0feea3fa52"]    @{FORM-DATA-E-LINE-EPL}[2]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
    Input Text    xpath://*[@id="id_bea6074c-891b-435d-b487-f20edbddcf88"]    @{FORM-DATA-E-LINE-EPL}[3]
    Input Text    xpath://*[@id="id_5d2fff5d-6370-483e-872b-f21a5a2d0f2b"]    @{FORM-DATA-E-LINE-EPL}[4]
    Input Text    id=id_bd9009ae-e2ad-443a-abaf-0b86fba3f98f    @{FORM-DATA-E-LINE-EPL}[5]
    Press Key    id=id_bd9009ae-e2ad-443a-abaf-0b86fba3f98f    \\09
    Input Text    xpath://*[@id="id_e23e3dd7-9024-42f4-85a4-3dc2e80df503"]    @{FORM-DATA-E-LINE-EPL}[6]
    Press Key    xpath://*[@id="id_e23e3dd7-9024-42f4-85a4-3dc2e80df503"]    \\09
    Input Text    xpath://*[@id="id_7a930a5d-69c9-4d5d-9d7a-0d6567d31de2"]    @{FORM-DATA-E-LINE-EPL}[7]
    Press Key    xpath://*[@id="id_7a930a5d-69c9-4d5d-9d7a-0d6567d31de2"]    \\09
    Input Text    xpath://*[@id="id_ba25bedd-aa08-47d8-92c1-6518c3efb1b0"]    @{FORM-DATA-E-LINE-EPL}[8]
    Select From List By Value    xpath://*[@id="id_6fe6f110-2918-43a9-9d6a-b53364b4fdcd"]    @{FORM-DATA-E-LINE-EPL}[9]
    Select From List By Value    xpath://*[@id="id_60fb3968-a44e-4436-957c-ee080d0ef689"]    @{FORM-DATA-E-LINE-EPL}[10]
    sleep    2s

Submit Forum
    Click Button    xpath://*[@id="phui-modal-actions"]/button
    sleep    2s
    Handle Alert    action=ACCEPT

Navigate To Job Manager Page
    Click Link    xpath://*[@id="activejobs"]/a
    sleep    10s

Choose Top Job Inside Job Manager Page
    Click Element    xpath://*[@id="jobs_table_body"]/tr[1]

CheckBox Auto Work Tasks
    Click Element    id=auto-work-tasks
