import json
import gspread
import time
import requests
import datetime
from datetime import date
from oauth2client.service_account import ServiceAccountCredentials

json_key = json.load(open('creds.json'))
config = json.load(open('config.json'))
scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

file = gspread.authorize(credentials) # authenticate with Google

start1 = date(2019, 4, 10)
start2 = date(2019, 1, 17)

# START UNIQUE PLAYERS
sheet = file.open("Population Over Time").get_worksheet(3) # open sheet

now = datetime.datetime.now().date()
deltaOffset = (now - start1).days
position = 66
for server in config['servers']:
    url = 'https://api.battlemetrics.com/servers/' + server['serverID']
    r = requests.get(url + f'/unique-player-history?start={now.year:04d}-{now.month:02d}-{now.day-1:02d}T12%3A00%3A00Z&stop={now.year:04d}-{now.month:02d}-{now.day:02d}T12%3A00%3A00Z', params=None)
    counter = deltaOffset - 1
    print (server['serverID'])
    try:
        sheet.update_acell(str(chr(position)) + "2", server['serverID'])
    except:
        print("RATE LIMIT EXCEEDED")

    for date in r.json()['data']:

        if position == 66:
            try:
                sheet.update_acell(str(chr(65)) + str(counter + 2), date['attributes']['timestamp'])
                print(date['attributes']['timestamp'])
                time.sleep(0.5)
            except:
                print("RATE LIMIT EXCEEDED")
        try:
            sheet.update_acell(str(chr(position)) + str(counter + 2), date['attributes']['value'])
            print(date['attributes']['value'])
        except:
            print("RATE LIMIT EXCEEDED")

        counter += 1
        time.sleep(1)
    position += 1
# END UNIQUE PLAYERS
print("-------")
time.sleep(5)
print("-------")
# START PLAYER COUNT
sheet = file.open("Population Over Time").get_worksheet(4) # open sheet

now = datetime.datetime.now().date()
deltaOffset = (now - start2).days
position = 66

for server in config['servers']:
    url = 'https://api.battlemetrics.com/servers/' + server['serverID']
    r = requests.get(url + f'/time-played-history?start={now.year:04d}-{now.month:02d}-{now.day-1:02d}T12%3A00%3A00Z&stop={now.year:04d}-{now.month:02d}-{now.day:02d}T12%3A00%3A00Z', params=None)
    counter = deltaOffset - 1
    print (server['serverID'])
    try:
        sheet.update_acell(str(chr(position)) + "2", server['serverID'])
    except:
        print("RATE LIMIT EXCEEDED")

    for date in r.json()['data']:

        if position == 66:
            try:
                sheet.update_acell(str(chr(65)) + str(counter + 2), date['attributes']['timestamp'])
                print(date['attributes']['timestamp'])
                time.sleep(0.5)
            except:
                print("RATE LIMIT EXCEEDED")
        try:
            sheet.update_acell(str(chr(position)) + str(counter + 2), int(date['attributes']['value']/3600))
            print(int(date['attributes']['value']/3600))
        except:
            print("RATE LIMIT EXCEEDED")

        counter += 1
        time.sleep(1)
    position += 1
# END PLAYER COUNT
