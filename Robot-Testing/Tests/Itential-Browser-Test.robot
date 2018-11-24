*** Settings ***
Documentation     Itential LGI R&D Lab (Browser Test)
Resource   C:/Python27/NSO-Testing/Resources/ItentialApp.robot

*** Test Cases ***
TC1
    [Documentation]    Testing Itential Pronghorn for E-Line EPL Service using (Chrome) Browser
    [Tags]    E-Line-EPL
    Begin Test With Chrome
    Go To PH Login
    Input Username and Password PH Login Page
    Navigate to Service Catalog Page
    Navigate To ELINE-EPL Form
    Populate E-LINE EPL Forum With Service Parameters
    Populate EPL Forum With Device Name: lg-ciena-3916-A
    Submit Forum
    Navigate To Job Manager Page
    Choose Top Job Inside Job Manager Page
    CheckBox Auto Work Tasks
TC2
    [Documentation]    Testing Itential Pronghorn for E-Line EVPL Service using (Chrome) Browser
    [Tags]    E-Line-EVPL
    Begin Test With Chrome
    Go To PH Login
    Input Username and Password PH Login Page
    Navigate to Service Catalog Page
    Navigate To ELINE-EVPL Form
    Populate E-LINE EVPL Forum With Service Parameters
    Populate EVPL Forum With Device Name: lg-ciena-3916-A
    Populate EVPL Forum With Bandwidth-Profile Service Parameters: VS Based
    Submit Forum E-LINE EVPL
    Navigate To Job Manager Page
    Choose Top Job Inside Job Manager Page
    CheckBox Auto Work Tasks

TC3
    [Documentation]    Testing Itential Pronghorn for E-Line EPL Service using (Chrome) Browser
    [Tags]    E-LAN-EPL
    Begin Test With Chrome
    Go To PH Login
    Input Username and Password PH Login Page
    Navigate to Service Catalog Page
    Navigate To ELAN-EPL Form
    Populate E-LAN EPL Forum With Service Parameters
    Populate E-LAN EPL Forum With Device Name: lg-ciena-3916-A
    Submit Forum
    Navigate To Job Manager Page
    Choose Top Job Inside Job Manager Page
    CheckBox Auto Work Tasks

TC4
    [Documentation]    Testing Itential Pronghorn for E-Line EPL Service using (Internet Explorer) Browser
    [Tags]    E-LAN-EPL
    Begin Test With IE
    Go To PH Login
    Input Username and Password PH Login Page
    Navigate to Service Catalog Page
    Navigate To ELAN-EPL Form
    Populate E-LAN EPL Forum With Service Parameters
    Populate E-LAN EPL Forum With Device Name: lg-ciena-3916-A
    Submit Forum
    Navigate To Job Manager Page
    Choose Top Job Inside Job Manager Page
    CheckBox Auto Work Tasks