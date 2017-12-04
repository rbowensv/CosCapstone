import time
from beacontools import BeaconScanner, IBeaconFilter
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import pytz

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
present=False
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def callback(bt_addr, rssi, packet, additional_info):
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
    if(packet.minor==22144):
        ##email(user,password,destination)
        global present
        present=True
def email(user, password, destination):
    

    s=smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(user,password)

    msg = MIMEMultipart()

    message='The Resident is missing and has no appointment'

    msg['From']=user

    msg["To"]=destination

    msg['Subject']='This is a TEST'

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)

    del msg

# scan for all iBeacon advertisements from beacons with the specified uuid
user=input("Email Username: ")
password=input("Email Password: ")

destination=input("Email Deastination: ")
delay=int(input("Delay between Scans: "))
timesToRepeat=int(input("Times to repeat: "))

"""Shows basic usage of the Google Calendar API.

Creates a Google Calendar API service object and outputs a list of the next
10 events on the user's calendar.
"""
    
tz = pytz.timezone('US/Eastern')
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

#while True:
for x in range(0,timesToRepeat):
    present=False
    now = datetime.datetime.now()

    the_datetime = tz.localize(now)
    the_datetime2 = tz.localize(now+datetime.timedelta(minutes = 10))
    body = {
      "timeMin": the_datetime.isoformat(),
      "timeMax": the_datetime2.isoformat(),
      "timeZone": 'US/Eastern',
      "items": [{"id": 'rbowensv@gmail.com'}]
    }

    eventsResult = service.freebusy().query(body=body).execute()
    cal_dict = eventsResult[u'calendars']
    busyResult = eventsResult["calendars"]["rbowensv@gmail.com"]["busy"]

    scanner = BeaconScanner(callback,
    device_filter=IBeaconFilter(uuid="61687109-905f-4436-91f8-e602f514c96d"))
    scanner.start()
    print("scanner started")
    time.sleep(5)
    scanner.stop()
    print("scanner stopped")
    if not present:
        print("Resident is not Present")
        if len(busyResult)==0:
            print("Resident is also not busy")
            email(user,password,destination)
        else:
            print("Resident is Busy, no email sent")
    else:
        print("Resident is Present")
    
    time.sleep(delay)