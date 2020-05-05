import pygsheets
import copy
import pickle
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import *

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

# calendar_colors = {
#     "Lavender"  : 1
#     "Sage"      : 2
#     "Grape"     : 3
#     "Flamingo"  : 4 #changes made by me
#     "Banana"    : 5 #holla
#     "Tangerine" : 6
#     "Peacock"   : 7
#     "Grapite"   : 8
#     "Blueberry" : 9
#     "Basil"     : 10
#     "Tomato"    : 11
# }

now = datetime.now()


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


# makes available the google sheet
gc = pygsheets.authorize(
    client_secret="/Users/adamdenhaan/Desktop/Experiment/client_secret_145372556979-b6di5pm67tdbpmipr6al0mein5eeq1aq.apps.googleusercontent.com.json",
    credentials_directory="/Users/adamdenhaan/Desktop/Experiment")
sh = gc.open_by_key("1UpfKu7Hrn8_-gR9BGGmM8s8dth3EAVVvx4sBybGNAHI")

# makes available the google calendar
scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file(
    "/Users/adamdenhaan/Desktop/Experiment/client_secret_728152513941-fldfta8n2c25rm77k8c836ldvmlnk4ub.apps.googleusercontent.com.json",
    scopes=scopes)
# credentials = flow.run_console()                      #to be run once
# pickle.dump(credentials, open("token.pkl", "wb"))     #to be run once
credentials = pickle.load(open("/Users/adamdenhaan/Desktop/Experiment/token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)

# delete future events
timeMin = now.isoformat('T') + "-05:00"
timeMax = (now + timedelta(days=90)).isoformat('T') + "-05:00"  # 90 days into the future to look for events to delete
result = service.events().list(calendarId="adamdh00@gmail.com", timeMin=timeMin, timeMax=timeMax).execute()
for i in range(0, len(result['items'])):
    try:
        if result['items'][i]['description'] == 'Automatic creation':
            service.events().delete(calendarId="adamdh00@gmail.com", eventId=result['items'][i]['id']).execute()
    except:
        pass

# use only the event sheet within the workbook
events_sheet = copy.deepcopy(sh[1])

my_events = events_sheet.find("ADH", cols=(7, 9))  # .find() can be restricted to only a certain row.

my_events_rows = []
for i in range(0, len(my_events)):
    row = my_events[i].row
    my_events_rows.append(row - 1)

dates = events_sheet.get_col(1)
titles = events_sheet.get_col(2)
calls = events_sheet.get_col(3)
ends = events_sheet.get_col(5)
locations = events_sheet.get_col(6)

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
    if hasNumbers(call_string):
        start_hour = int(call_string.split(':')[0])
        start_minute = int(call_string.split(':')[1][0:2])
        if call_string.split(':')[1][-2:] == "PM" and start_hour != 12:
            start_hour += 12
    else:
        start_hour = 13
        start_minute = 30

    # end hour and minute ints
    end_string = ends[i]
    if hasNumbers(end_string):
        end_hour = int(end_string.split(':')[0])
        end_minute = int(end_string.split(':')[1][0:2])
        if end_string.split(':')[1][-2:] == "PM" and end_hour != 12:
            end_hour += 12
    else:
        end_hour = 23
        end_minute = 59

    # location string
    location = locations[i]

    # # for testing
    # print("Name: " + name)
    # print("Year: " + str(year))
    # print("month: " + str(month))
    # print("date: " + str(date))
    # print("start hour: " + str(start_hour))
    # print("start minute: " + str(start_minute))
    # print("end hour: " + str(end_hour))
    # print("end minute: " + str(end_minute))
    # print("location: " + location)

    # create the calendar event
    start_time = datetime(year, month, date, start_hour, start_minute, 0)
    end_time = datetime(year, month, date, end_hour, end_minute, 0)
    calevent = {
        'summary': name,
        'location': location,
        'colorId': 11,  # where you can select the color of the event
        'description': 'Automatic creation',
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
    if hasNumbers(end_string) and now < start_time:
        service.events().insert(calendarId="adamdh00@gmail.com", body=calevent).execute()  # DANGER LINE
        # pass          # here for when the previous line is commented out
