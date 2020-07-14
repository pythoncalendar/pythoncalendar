'''a functionified version of v2
By Adam DenHaan
Jun 15, 2020

calendar_colors = {
    "Lavender"  : 1
    "Sage"      : 2
    "Grape"     : 3
    "Flamingo"  : 4
    "Banana"    : 5
    "Tangerine" : 6
    "Peacock"   : 7
    "Grapite"   : 8
    "Blueberry" : 9
    "Basil"     : 10
    "Tomato"    : 11
}

'''

import pygsheets
import copy
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
from time import sleep

def calhelp(initials, calendarId, directory, sheet_secret_name, cal_secret_name, colorID = 11):
    """designed to facilitate the use of v2

    Args:
        initials (string): intials to search for on the sheet
        calendarId (string): calendar ID of the calendar to write events to
        directory (string): location of where to store credential files
        sheet_secret_name (string): filename of the sheet secret name
        cal_secret_name (string): filename of the calendar secret name
        colorID (int, optional): color of the events on the calendar. Defaults to 11.
    """

    months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
        }

    hasnumbers = lambda inputstring: any(char.isdigit() for char in inputstring)

    now = datetime.now()

    # makes available the google sheet
    gc = pygsheets.authorize(
        client_secret= directory + "/" + sheet_secret_name,
        credentials_directory=directory,
        local=True)
    sh = gc.open_by_key("1UpfKu7Hrn8_-gR9BGGmM8s8dth3EAVVvx4sBybGNAHI")

    # makes available the google calendar
    pklstr = directory + '/token.pkl'
    scopes = ['https://www.googleapis.com/auth/calendar']
    if os.path.exists(pklstr):
        with open(pklstr, "rb") as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
        directory + "/" + cal_secret_name,
        scopes=scopes)
        credentials = flow.run_local_server(port=0)
        with open(pklstr, "wb") as token:
            pickle.dump(credentials, token)    
    service = build("calendar", "v3", credentials=credentials)

    while True:
        j = 0
        # delete future events
        timeMin = now.isoformat('T') + "-05:00"
        timeMax = (now + timedelta(days=90)).isoformat('T') + "-05:00"  # 90 days into the future to look for events to delete
        result = service.events().list(calendarId=calendarId, timeMin=timeMin, timeMax=timeMax).execute() #pylint: disable=no-member
        delete_events_id = []
        for i in range(0, len(result['items'])):
            try:
                if result['items'][i]['description'][:18] == 'Automatic creation':
                    delete_events_id.append(result['items'][i]['id'])
            except:     #not all event have a feild 'description', and raises an error if there is no feild. Addressed by skipping event as its not ours
                pass


        for i in delete_events_id:
            try:
                service.events().delete(calendarId=calendarId, eventId = i).execute() #pylint: disable=no-member
                j += 1
            except:
                sleep(1)
                service.events().delete(calendarId=calendarId, eventId = i).execute() #pylint: disable=no-member
                j += 1
        if j == 0:
            break

    # use only the event sheet within the workbook
    events_sheet = copy.deepcopy(sh[1])
    contact_list = copy.deepcopy(sh[3])

    my_events_rows = []
    my_events = events_sheet.find(initials, cols=(7, 9) ) 
    for i in range(0, len(my_events)):
        row = my_events[i].row
        my_events_rows.append(row - 1)

    everyone_events = events_sheet.find('ALL', cols=(1,7), matchEntireCell = True)
    for i in range(0, len(everyone_events)):
        row = everyone_events[i].row
        my_events_rows.append(row - 1)

    dates           = events_sheet.get_col(1)
    titles          = events_sheet.get_col(2)
    calls           = events_sheet.get_col(3)
    starts          = events_sheet.get_col(4)
    ends            = events_sheet.get_col(5)
    locations       = events_sheet.get_col(6)
    records         = events_sheet.get_col(8)
    event_coords    = events_sheet.get_col(14)
    coord_names     = contact_list.get_col(1)
    coord_nums      = contact_list.get_col(4)

    coord_dict = {}
    for i in range(2, 11):
        coord_dict[coord_names[i]] = coord_nums[i]
    for i in range(72,75):
        coord_dict[coord_names[i]] = coord_nums[i]

    for i in my_events_rows:

        # year/month/date ints
        month = months[dates[i][5:8]]
        year = now.year
        if now.month >= 8:
            if month < 8:
                year += 1
        else:
            if month >= 8:
                year -= 1
        date = int(dates[i][-2:])

        # event title string
        name = titles[i]

        # call hour and minute ints
        call_string = calls[i]
        if hasnumbers(call_string):
            start_hour = int(call_string.split(':')[0])
            start_minute = int(call_string.split(':')[1][0:2])
            if call_string.split(':')[1][-2:] == "PM" and start_hour != 12:
                start_hour += 12
        else:
            start_hour = 13
            start_minute = 30

        # end hour and minute ints
        end_string = ends[i]
        if hasnumbers(end_string):
            end_hour = int(end_string.split(':')[0])
            end_minute = int(end_string.split(':')[1][0:2])
            if end_string.split(':')[1][-2:] == "PM" and end_hour != 12:
                end_hour += 12
        else:
            end_hour = 23
            end_minute = 59

        # location string
        location = locations[i]

        #record string
        if records[i] == "Yes":
            record = "Yes"
        else:
            record = "No"

        #start string
        start = starts[i]

        # Event coordinator string
        event_coord = event_coords[i]

        # Event coordinator phone
        try:
            coord_num = coord_dict[event_coord]
        except:
            coord_num = "N/A"

        # Description string
        descripion = ('Automatic creation\nEvent Start Time: ' + start + 
            '\nEvent Coordinator: ' + event_coord + 
            '\nEvent Coordinator Number: ' + coord_num + 
            '\nRecord: ' + record)

        # create the calendar event
        start_time = datetime(year, month, date, start_hour, start_minute, 0)
        end_time = datetime(year, month, date, end_hour, end_minute, 0)
        calevent = {
            'summary': name,
            'location': location,
            'colorId': colorID,          # where you can select the color of the event
            'description': descripion,
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': "America/New_York",
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': "America/New_York",
            },
            'reminders': {
                'useDefault': True,
            },
        }

        # adds calendar event
        if hasnumbers(end_string) and now < start_time:
            try:
                service.events().insert(calendarId=calendarId, body=calevent).execute() #pylint: disable=no-member
            except:
                sleep(1)
                service.events().insert(calendarId=calendarId, body=calevent).execute() #pylint: disable=no-member


if __name__ == '__main__':
    calhelp(initials="ADH",
    calendarId="adamdh00@gmail.com",
    directory="/Users/adamdenhaan/Documents/pycalauth",
    sheet_secret_name="client_secret_145372556979-b6di5pm67tdbpmipr6al0mein5eeq1aq.apps.googleusercontent.com.json",
    cal_secret_name="client_secret_728152513941-fldfta8n2c25rm77k8c836ldvmlnk4ub.apps.googleusercontent.com.json",
    colorID=11)