*** settings ***
Suite Teardown    Delete All Sessions
Library           Collections
Library           String
Library           OperatingSystem
Library           RequestsLibrary
Library           REST

*** Variables ***
${user}           nsoadmin
${passwd}         nsoadmin
&{headers}        Content-Type=application/yang-data+xml    Accept=application/yang-data+xml
&{headers-json}    Content-Type=application/yang-data+json    Accept=application/yang-data+json

*** test cases ***
Post Requests to create NSO service using data.xml file
    [Tags]    ASPAN1
    ${data}=    Get Binary File    API/XML/data.xml
    ${auth}=    Create List    ${user}    ${passwd}
    Create Session    alias=NSO    url=http://192.168.204.128:8080    headers=${headers}    auth=${auth}
    ${resp}=    Post Request    NSO    /restconf/data/services    data=${data}
    Should Be Equal As Strings    ${resp.status_code}    201

Check Service in NS if contains devCISCO-2
    [Tags]    ASPAN
    ${auth}=    Create List    ${user}    ${passwd}
    Create Session    alias=NSO    url=http://192.168.204.128:8080    headers=${headers}    auth=${auth}
    ${result}=    Get Request    NSO    /restconf/data/services
    Should Be Equal    ${result.status_code}    ${200}
    ${result-data}=    Set Variable    ${result.text}
    Should Contain    ${result-data}    devCISCO-2
    Should Contain    ${result-data}    Test1
    Should Contain    ${result-data}    NONO
    Should Contain    ${result-data}    NL
    log to console    ${result-data}
