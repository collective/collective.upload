*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${cancel_button_selector} =  button.cancel
@{images} =  640px-Mandel_zoom_00_mandelbrot_set.jpg  640px-Mandel_zoom_04_seehorse_tail.jpg  640px-Mandel_zoom_06_double_hook.jpg  640px-Mandel_zoom_07_satellite.jpg  640px-Mandel_zoom_12_satellite_spirally_wheel_with_julia_islands.jpg
${exif_description} =  Belém (Brazil)
${exif_rights} =  Daniel Zanini H.

*** Test cases ***

Test Cancel First
    Enable Autologin as  Site Administrator
    Goto Homepage

    Add files
    Cancel first file


Test Cancel All
    Enable Autologin as  Site Administrator
    Goto Homepage

    Add files
    Cancel all files


Test Upload
    Enable Autologin as  Site Administrator
    Goto Homepage

    Add files
    Start upload


Test EXIF
    Enable Autologin as  Site Administrator
    Goto Homepage

    Click Add Multiple Files

    # For some reason this code warm up the upload and avoid errors
    Choose File  css=input[type=file]  /tmp/Belem.jpg
    Sleep  1s  Wait for image to load

    Choose File  css=input[type=file]  /tmp/Belem.jpg
    Page Should Contain Element  css=input[type=text][value="Belem.jpg"]

    Click Button  css=.fileupload-buttonbar .start
    Wait Until Page Does Not Contain  Add files…

    Page Should Contain  Belem.jpg
    Click Link  Belem.jpg
    Page Should Contain  ${exif_description}
    Page Should Contain  ${exif_rights}

*** Keywords ***

Click Add Multiple Files
    Open Add New Menu
    Click Link  css=a#multiple-files
    wait until page contains  Add files…

Add files
    Click Add Multiple Files

    # For some reason this code warm up the upload and avoid errors
    Choose File  css=input[type=file]  /tmp/640px-Mandel_zoom_00_mandelbrot_set.jpg
    Sleep  1s  Wait for image to load

    : FOR  ${image}  IN  @{images}
    \  Choose File  css=input[type=file]  /tmp/${image}
    \  Page Should Contain Element  css=input[type=text][value="${image}"]

Cancel first file
    Click Button  css=.template-upload:first-child .cancel
    # use size of first image as trigger
    Wait Until Page Does Not Contain  28.69 KB
    Click Button  css=.fileupload-buttonbar .start

    Wait Until Page Does Not Contain  Add files…

    Page Should Not Contain  @{images}[0]
    Page Should Contain  @{images}[1]

Cancel all files
    Click Button  css=.fileupload-buttonbar .cancel
    # use size of last image as trigger
    Wait Until Page Does Not Contain  90.11 KB

    Wait Until Page Does Not Contain  Add files…

    : FOR  ${image}  IN  @{images}
    \  Page Should Not Contain  ${image}

Start upload
    Click Button  css=.fileupload-buttonbar .start

    Wait Until Page Does Not Contain  Add files…

    Goto Homepage

    : FOR  ${image}  IN  @{images}
    \  Page Should Contain  ${image}
