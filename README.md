# PyCal

PyCal is a python script designed to take events on the Calvin Event Services calendar and port specific events to your personal calendar. Note that this is only compatible with Google's Calendar service.

## Prerequisites

1) Be sure that Python 3.x is installed on your machine. This program has been tested with 3.7.x and 3.8.x. See [Python 3 Installation & Setup Guide](https://realpython.com/installing-python/).

2) Be sure the latest version of [pip](https://pip.pypa.io/en/stable/) is installed on your machine.

3) Install pip package [pygsheets](https://pygsheets.readthedocs.io/en/stable/) is installed on your machine using the terminal:

   ```bash
   pip install pygsheets
   ``` 

4) Download pythoncalendar_v3.py.

# Usage

1) Find a directory where you can store multiple files, and forget about them. A typical solution is to create a directory in your documents directory, and name it PyCal.

    * Move pythoncalendar_v3.py here, and create another directory within PyCal and name it "credentials".

2) Set up the [Google Developers Console](https://console.developers.google.com/) for your **school** account. 

    1) Be sure you are logged into your school account (xxx##@students.calvin.edu).
    2) Agree to terms and services if you haven't already.
    3) In the top left, click "Select a project", and then hit "NEW PROJECT".
    4) Keep the default name, organization, and location of the project, and hit "CREATE".
    5) After you are "in" your new project, hit "ENABLE APIS AND SERVICES" on the dashboard. Search for Google Sheets API and hit enable.
    6) After enabling, go back to the dashboard by hitting the three lines on the top left corner, APIs and Services > Dashboard.
    7) On the left, click OAuth consent screen, hit Internal, and hit Create. Under Application Name, name it "PyCal, School Account". This will serve to remind you later to log into you school account as opposed to any other account. Leaving all other feilds in their default state, hit Save at the bottom.
    8) On the left, click Credentials, and then "CREATE CREDENTIALS" > OAuth Client ID. Application type: Desktop App. You may keep the default name, and then hit CREATE, and OK.
    9) Back on the dashboard under "OAuth 2.0 Client IDs", click the download button on the right side of the screen. Move this to your credentials folder created earlier, and for convenience rename as "SCS.json".

3) Set up the [Google Developers Console](https://console.developers.google.com/) for your **personal** account. This is similar to step 2 in many ways. If you want the events to school up on your google calendar registered with your Calvin email, skip steps 1-4 of below:

    1) Be sure you are logged into your personal account (or whichever account you would like the events to show up on).
    2) Agree to terms and services if you haven't already.
    3) In the top left, click "Select a project", and then hit "NEW PROJECT".
    4) Keep the default name, organization, and location of the project, and hit "CREATE".
    5) After you are "in" your new project, hit "ENABLE APIS AND SERVICES" on the dashboard. Search for Google Calendar API and hit enable.
    6) After enabling, go back to the dashboard by hitting the three lines on the top left corner, APIs and Services > Dashboard.
    7) On the left, click OAuth consent screen, hit External, and hit Create. Under Application Name, name it "PyCal, Calendar Account". This will serve to remind you later to log into you school account as opposed to any other account. Leaving all other feilds in their default state, hit Save at the bottom.
    8) On the left, click Credentials, and then "CREATE CREDENTIALS" > OAuth Client ID. Application type: Desktop App. You may keep the default name, and then hit CREATE, and OK.
    9) Back on the dashboard under "OAuth 2.0 Client IDs", click the download button on the right side of the screen. Move this to your credentials folder created earlier, and for convenience rename as "PCS.json".

4) Edit the python file for *your* use.
    
    1) Change you initials on line 237 to your intials exactly as they appear in the sheet. 
        ```python
        calhelp(initials="ADH",
        ```  
    2) Change the email on line 238 to be the email you logged into for set 3.1
        ```python
        calendarId="adamdh00@gmail.com",
        ``` 
    3) Change the path on line 239 to be the location of the folder you created in step 1
        ```python
        directory="/Users/adamdenhaan/Documents/PyCal",
        ``` 
    4) (optional) change the color id on line 242 to the color of your choosing, which are listed on lines 6-16
        ```python
        colorID=11)
        ``` 

5) Run the file. This can be done in many ways, here is an example in BASH/ZSH modeled after the info in step 4:
    ```Bash
        python3 /Users/adamdenhaan/Documents/PyCal/pythoncalendar_v3.py
    ```
    The first time you run this, you will be prompted to log in twice, first to your **school** account, and then to your **personal** account. After this, running the script will proceed automatically, and you can run after meetings, or whenever you would like your calendar update with the events.

6) (optional) Automate the execution of that BASH line. 

# Contact

Email [me](add22@students.calvin.edu) (Adam DenHaan) with subject "PyCal" with questions.

## Additional
The script is currently designed for the tech crew (sound & lighting), but can be easily adapted for other crews in event services, or any sheet in general. If you are code-savvy, lines 66, 110-111, and 124-133 can be modified to change the workbook, sheet, and column locations respectively.