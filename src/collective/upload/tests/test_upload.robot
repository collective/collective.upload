*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${cancel_button_selector} =  button.cancel
${close_button_selector} =  div.close a

*** Test cases ***

Test Upload
    [Tags]  Expected Failure
    Enable Autologin as  Site Administrator
    Goto Homepage

    Upload

*** Keywords ***

Click Add Multiple Files
    Open Add New Menu
    Click Link  css=a#multiple-files
    Wait Until Page Contains  Add files or images…

Upload
    Click Add Multiple Files
    # TODO
    Click Link  css=${close_button_selector}
    Wait Until Page Does Not Contain  Add files or images…
