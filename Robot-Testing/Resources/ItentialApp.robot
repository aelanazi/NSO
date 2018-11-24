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
...               1    100000    BE    None   88A8   8100
@{FORM-DATA-HOSTS}    lg-ciena-3916-A    lg-ciena-3916-B    lg-ciena-3916-C    lg-ciena-5142-A    lg-ciena-5160-A    lg-ciena-5160-B    lg-ciena-5160-C
@{FORM-DATA-BANDWIDTH-PROFILE}    VS Based    CVLAN Based    P-Bit Based

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
Navigate To CE-EACCESS-ELAN-ENNI Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[1]/td[3]/button
    sleep    2s
Navigate To EACCESS-ELINE-ENNI Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[2]/td[3]/button
    sleep    2s
Navigate To EACCESS-EPL Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[3]/td[3]/button
    sleep    2s
Navigate To EACCESS-EPLAN Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[4]/td[3]/button
    sleep    2s
Navigate To EACCESS-EVPL Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[5]/td[3]/button
    sleep    2s
Navigate To EACCESS-EVPLAN Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[6]/td[3]/button
    sleep    2s
Navigate To ELAN-EPL Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[7]/td[3]/button
    sleep    2s
Navigate To ELAN-EVPL Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[8]/td[3]/button
    sleep    2s
Navigate To ELINE-EPL Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[9]/td[3]/button
    sleep    2s
Navigate To ELINE-EVPL Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[10]/td[3]/button
    sleep    2s
Navigate To ETRANSIT-ELAN Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[11]/td[3]/button
    sleep    2s
Navigate To ETRANSIT-ELINE Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[12]/td[3]/button
    sleep    2s
Navigate To ETREE-EPL Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[13]/td[3]/button
    sleep    2s
Navigate To ETREE-EVPL Form
    Click Button    xpath:/html/body/div/div[1]/div[2]/table/tbody/tr[14]/td[3]/button
    sleep    2s
Populate E-LINE EPL Forum With Service Parameters
    Input Text    xpath://*[@id="id_354c7ebb-da8f-4267-b3aa-9b220581134b"]    @{FORM-DATA-E-LINE-EPL}[0]
    Input Text    xpath://*[@id="id_95a36447-bf81-4ad5-a0c3-0a98c22555e2"]    @{FORM-DATA-E-LINE-EPL}[1]
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
Populate E-LINE EVPL Forum With Service Parameters
    Input Text    xpath://*[@id="id_c24d5db3-52b5-478d-b396-05f92f8671e6"]    @{FORM-DATA-E-LINE-EPL}[0]
    Input Text    xpath://*[@id="id_9c0411dd-b39d-4c94-84e9-9522495e767b"]    @{FORM-DATA-E-LINE-EPL}[1]
    Input Text    xpath://*[@id="id_4a4c2927-235b-4cde-92f2-f4cae9850a26"]    @{FORM-DATA-E-LINE-EPL}[3]
    Input Text    xpath://*[@id="id_5df803c0-1a00-42ff-b34b-22781b4bb7be"]    @{FORM-DATA-E-LINE-EPL}[4]
    Input Text    xpath://*[@id="id_d3d97314-8aa5-49fd-8b6a-e8a74afcefeb"]    @{FORM-DATA-E-LINE-EPL}[5]
    Press Key     xpath://*[@id="id_d3d97314-8aa5-49fd-8b6a-e8a74afcefeb"]    \\09
    Input Text    xpath://*[@id="id_a524d7fe-2d37-4e57-8cbe-4155c74befb5"]    @{FORM-DATA-E-LINE-EPL}[6]
    Press Key     xpath://*[@id="id_a524d7fe-2d37-4e57-8cbe-4155c74befb5"]    \\09
    Input Text    xpath://*[@id="id_ddd345b8-8520-418b-9f9c-ae30f61c9b00"]    @{FORM-DATA-E-LINE-EPL}[7]
    Press Key     xpath://*[@id="id_ddd345b8-8520-418b-9f9c-ae30f61c9b00"]    \\09
    Select From List By Value    xpath://*[@id="id_7cb4bb49-56c6-42a4-8b5e-d10ab328ca33"]    @{FORM-DATA-E-LINE-EPL}[11]
    Select From List By Value    xpath://*[@id="id_0107a4cc-ecc7-49dc-8aee-de7290542f0b"]    @{FORM-DATA-E-LINE-EPL}[10]
    Select From List By Value    xpath://*[@id="id_d08b1f78-a69c-45bd-803c-139860665810"]    @{FORM-DATA-BANDWIDTH-PROFILE}[0]
Populate EVPL Forum With Bandwidth-Profile Service Parameters: VS Based
    Select From List By Value    xpath://*[@id="id_d08b1f78-a69c-45bd-803c-139860665810"]    @{FORM-DATA-BANDWIDTH-PROFILE}[0]
    Select From List By Value    xpath://*[@id="id_8fd7b068-3f39-40ea-b545-eb1f2eb615e6"]    @{FORM-DATA-E-LINE-EPL}[9]
    Input Text    xpath://*[@id="id_ff79f596-5c53-4315-bd73-a6761a378f7b"]    @{FORM-DATA-E-LINE-EPL}[8]
    Input Text    xpath://*[@id="id_00df20f2-09b3-42be-8964-eb32de7b29e7"]    100-102
Populate EVPL Forum With Bandwidth-Profile Service Parameters: CVLAN Based
    Select From List By Value    xpath://*[@id="id_d08b1f78-a69c-45bd-803c-139860665810"]    @{FORM-DATA-BANDWIDTH-PROFILE}[1]
Populate EVPL Forum With Bandwidth-Profile Service Parameters: P-Bit Based
    Select From List By Value    xpath://*[@id="id_d08b1f78-a69c-45bd-803c-139860665810"]    @{FORM-DATA-BANDWIDTH-PROFILE}[2]
Populate E-LAN EPL Forum With Service Parameters
    Input Text    xpath://*[@id="id_3010e3c5-4490-4419-97fd-1d22fe0823cd"]    CUST1
    Input Text    xpath://*[@id="id_012aa81d-6538-4df8-8ec5-e729fafba2fd"]    SR-NL-991
    Input Text    xpath://*[@id="id_a1d16795-d0b8-4483-8a80-044e3b530ef5"]    110000101
    Input Text    xpath://*[@id="id_6898c48c-4184-40fa-8352-db59e12008d0"]    3
    Press Key     xpath://*[@id="id_6898c48c-4184-40fa-8352-db59e12008d0"]    \\09
    Input Text    xpath://*[@id="id_99a0a0e2-b8a6-43a8-b96c-536bf5ddd7cd"]    33
    Press Key     xpath://*[@id="id_99a0a0e2-b8a6-43a8-b96c-536bf5ddd7cd"]    \\09
    Input Text    xpath://*[@id="id_16251000-6efd-44bd-810e-33211a4cf7a9"]    89
    Press Key     xpath://*[@id="id_16251000-6efd-44bd-810e-33211a4cf7a9"]    \\09
    Input Text    xpath://*[@id="id_169f8c69-9d12-41aa-80e6-c9c6c527d47e"]    100000
    Press Key     xpath://*[@id="id_169f8c69-9d12-41aa-80e6-c9c6c527d47e"]    \\09
    Input Text    xpath://*[@id="id_c837ce3f-68cc-40f3-9e50-7687e7a87472"]   8
    Press Key     xpath://*[@id="id_c837ce3f-68cc-40f3-9e50-7687e7a87472"]   \\09
    Select From List By Value    xpath://*[@id="id_208b294b-9755-4a06-93af-d78fe4ff4c6a"]    @{FORM-DATA-E-LINE-EPL}[9]
    Select From List By Value    xpath://*[@id="id_a181f0f1-16d8-40c5-84ae-15689ca2e98a"]    @{FORM-DATA-E-LINE-EPL}[10]
    sleep    2s

Populate E-LAN EPL Forum With Device Name: lg-ciena-3916-A
    Input Text    xpath://*[@id="id_4c68e737-b4bd-4faf-84b8-467ec7e9dc18"]    @{FORM-DATA-HOSTS}[0]
    Click Button  xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
    sleep    2s

Populate EPL Forum With Device Name: lg-ciena-3916-A
    Input Text    xpath://*[@id="id_5e5d9068-479f-4d02-b1d1-3a0feea3fa52"]    @{FORM-DATA-HOSTS}[0]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
    sleep    2s
Populate EPL Forum With Device Name: lg-ciena-3916-B
    Input Text    xpath://*[@id="id_5e5d9068-479f-4d02-b1d1-3a0feea3fa52"]    @{FORM-DATA-HOSTS}[1]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
Populate EPL Forum With Device Name: lg-ciena-3916-C
    Input Text    xpath://*[@id="id_5e5d9068-479f-4d02-b1d1-3a0feea3fa52"]    @{FORM-DATA-HOSTS}[2]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
Populate EPL Forum With Device Name: lg-ciena-5142-A
    Input Text    xpath://*[@id="id_5e5d9068-479f-4d02-b1d1-3a0feea3fa52"]    @{FORM-DATA-HOSTS}[3]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
Populate EPL Forum With Device Name: lg-ciena-5160-A
    Input Text    xpath://*[@id="id_5e5d9068-479f-4d02-b1d1-3a0feea3fa52"]    @{FORM-DATA-HOSTS}[4]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
Populate EPL Forum With Device Name: lg-ciena-5160-B
    Input Text    xpath://*[@id="id_5e5d9068-479f-4d02-b1d1-3a0feea3fa52"]    @{FORM-DATA-HOSTS}[5]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
Populate EPL Forum With Device Name: lg-ciena-5160-C
    Input Text    xpath://*[@id="id_5e5d9068-479f-4d02-b1d1-3a0feea3fa52"]    @{FORM-DATA-HOSTS}[6]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button

Populate EVPL Forum With Device Name: lg-ciena-3916-A
    Input Text    xpath://*[@id="id_ad9c8279-1021-4bee-b532-6bfe8144e606"]   @{FORM-DATA-HOSTS}[0]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
Populate EVPL Forum With Device Name: lg-ciena-3916-B
    Input Text    xpath://*[@id="id_ad9c8279-1021-4bee-b532-6bfe8144e606"]    @{FORM-DATA-HOSTS}[1]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
Populate EVPL Forum With Device Name: lg-ciena-3916-C
    Input Text    xpath://*[@id="id_ad9c8279-1021-4bee-b532-6bfe8144e606"]    @{FORM-DATA-HOSTS}[2]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
Populate EVPL Forum With Device Name: lg-ciena-5142-A
    Input Text    xpath://*[@id="id_ad9c8279-1021-4bee-b532-6bfe8144e606"]    @{FORM-DATA-HOSTS}[3]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
Populate EVPL Forum With Device Name: lg-ciena-5160-A
    Input Text    xpath://*[@id="id_ad9c8279-1021-4bee-b532-6bfe8144e606"]    @{FORM-DATA-HOSTS}[4]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
Populate EVPL Forum With Device Name: lg-ciena-5160-B
    Input Text    xpath://*[@id="id_ad9c8279-1021-4bee-b532-6bfe8144e606"]    @{FORM-DATA-HOSTS}[5]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button
Populate EVPL Forum With Device Name: lg-ciena-5160-C
    Input Text    xpath://*[@id="id_ad9c8279-1021-4bee-b532-6bfe8144e606"]    @{FORM-DATA-HOSTS}[6]
    Click Button    xpath://*[@id="id_cont-jaxwvryy"]/div/ul/li[1]/div/div/button


Submit Forum
    Click Button    xpath://*[@id="phui-modal-actions"]/button
    sleep    2s
    Handle Alert    action=ACCEPT

Submit Forum E-LINE EVPL
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
