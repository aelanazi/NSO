*** Settings ***
Documentation     Itential LGI R&D Lab (Browser Test)
Resource   C:/Python27/NSO-Testing/Resources/ItentialApp.robot

*** Test Cases ***
TC1
    [Documentation]    Testing Itential Pronghorn for E-Line EPL Service using (Chrome) Browser
    [Tags]    CHROME
    Begin Test With Chrome
    Go To PH Login
    Input Username and Password PH Login Page
    Navigate to Service Catalog Page
    Navigate to E-Line EPL Form
    Populate E-Line EPL Forum With Service Parameters
    Submit Forum
    Navigate To Job Manager Page
    Choose Top Job Inside Job Manager Page
    CheckBox Auto Work Tasks

TC2
    [Documentation]    Testing Itential Pronghorn for E-Line EPL Service using (Internet Explorer) Browser
    [Tags]    IE
    Begin Test With IE
    Go To PH Login
    Input Username And Password PH Login Page
    Navigate To Service Catalog Page
    Navigate To E-Line EPL Form
    Populate E-Line EPL Forum with Service Parameters
    Submit Forum
    Navigate To Job Manager Page
    Choose Top Job Inside Job Manager Page
    CheckBox Auto Work Tasks