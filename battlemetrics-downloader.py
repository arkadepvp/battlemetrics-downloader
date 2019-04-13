import json
import gspread
import time
import requests
from oauth2client.service_account import ServiceAccountCredentials

json_key = json.load(open('creds.json'))
config = json.load(open('config.json'))
scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

file = gspread.authorize(credentials) # authenticate with Google
sheet = file.open("Population Over Time").get_worksheet(1) # open sheet

all_cells = sheet.range('A1:B2')
print (all_cells)

position = 66
for server in config['servers']:
    url = 'https://api.battlemetrics.com/servers/' + server['serverID']
    r = requests.get(url + '/unique-player-history?start=2019-04-10T12%3A00%3A00Z&stop=2019-04-14T12%3A00%3A00Z', params=None)
    counter = 1
    print (server['serverID'])
    try:
        sheet.update_acell(str(chr(position)) + "1", server['serverID'])
    except:
        print("RATE LIMIT EXCEEDED")

    for date in r.json()['data']:

        if position == 66:
            try:
                sheet.update_acell(str(chr(65)) + str(counter + 1), date['attributes']['timestamp'])
                print(date['attributes']['timestamp'])
            except:
                print("RATE LIMIT EXCEEDED")
        try:
            sheet.update_acell(str(chr(position)) + str(counter + 1), date['attributes']['value'])
            print(date['attributes']['value'])
        except:
            print("RATE LIMIT EXCEEDED")


        counter += 1
        time.sleep(.5)
    position += 1
