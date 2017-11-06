*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

@{upload_overlay_selector}  css=form.fileupload
${cancel_button_selector} =  button.cancel
@{images} =  640px-Mandel_zoom_00_mandelbrot_set.jpg  640px-Mandel_zoom_04_seehorse_tail.jpg  640px-Mandel_zoom_06_double_hook.jpg  640px-Mandel_zoom_07_satellite.jpg  640px-Mandel_zoom_12_satellite_spirally_wheel_with_julia_islands.jpg
${exif_description} =  Belém (Brazil)
${exif_rights} =  Daniel Zanini H.

*** Test cases ***

Test Cancel First
    Enable Autologin as  Site Administrator
    Goto Homepage

    Add Files  @{images}
    Cancel First File


Test Cancel All
    Enable Autologin as  Site Administrator
    Goto Homepage

    Add Files  @{images}
    Cancel All Files


Test Upload
    Enable Autologin as  Site Administrator
    Goto Homepage

    Add Files  @{images}
    Start Upload

    : FOR  ${image}  IN  @{images}
    \  Page Should Contain  ${image}


Test EXIF
    Enable Autologin as  Site Administrator
    Goto Homepage

    Click Add Multiple Files

    # need to slow down Selenium here to avoid errors on images
    ${speed} =  Set Selenium Speed  2 seconds

    Choose File  css=input[type=file]  /tmp/Belem.jpg
    Page Should Contain Element  css=input[type=text][value="Belem.jpg"]

    Set Selenium Speed  ${speed}

    Start Upload

    Page Should Contain  Belem.jpg
    Click Link  Belem.jpg
    Page Should Contain  ${exif_description}
    Page Should Contain  ${exif_rights}

*** Keywords ***

Click Add Multiple Files
    Open Add New Menu
    Click Link  css=a#multiple-files
    Wait Until Page Contains Element  @{upload_overlay_selector}

Add Files
    [Arguments]  @{files}

    Click Add Multiple Files

    # need to slow down Selenium here to avoid errors on images
    ${speed} =  Set Selenium Speed  2 seconds

    : FOR  ${file}  IN  @{files}
    \  Choose File  css=input[type=file]  /tmp/${file}
    \  Sleep  1s  Wait for file to load
    \  Page Should Contain Element  css=input[type=text][value="${file}"]

    Set Selenium Speed  ${speed}

Cancel First File
    Click Button  css=.template-upload:first-child .cancel
    # use size of first image as trigger
    Wait Until Page Does Not Contain  28.69 KB
    Click Button  css=.fileupload-buttonbar .start

    Wait Until Page Does Not Contain  Add files…

    Page Should Not Contain  @{images}[0]
    Page Should Contain  @{images}[1]

Cancel All Files
    Click Button  css=.fileupload-buttonbar .cancel
    # use size of last image as trigger
    Wait Until Page Does Not Contain  90.11 KB

    Wait Until Page Does Not Contain  Add files…

    : FOR  ${image}  IN  @{images}
    \  Page Should Not Contain  ${image}

Start Upload
    Click Button  css=.fileupload-buttonbar .start
    Wait Until Page Does Not Contain Element  @{upload_overlay_selector}
