*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote
Resource  Accessibility/wavetoolbar.robot

Suite setup  Run keywords
...  Open accessibility test browser  Maximize Browser Window
Suite teardown  Close all browsers

*** Test cases ***

Test A11Y
    [Documentation]  Test folder contents view for accessibility errors.
    Enable Autologin as  Site Administrator

    Go to Homepage
    Click Link  Contents
    ${url} =  Execute Javascript  window.location.href;

    ${errors} =  Count WAVE accessibility errors  ${url}
    Should be true  ${errors} <= 2
    ...  WAVE Toolbar reported ${errors} errors for ${url}
