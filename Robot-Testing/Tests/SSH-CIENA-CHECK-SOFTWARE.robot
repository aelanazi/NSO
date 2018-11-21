*** Settings ***
Library           SSHLibrary

*** Test Cases ***
Service-E-Line-Creation
    [Tags]    SSH
    SSHLibrary.Open Connection    172.30.150.195
    SSHLibrary.Login    aanazi    Rekord1982#
    SSHLibrary.Write    software show
    SSHLibrary.Read    delay=1s
