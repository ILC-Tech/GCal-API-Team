
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

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

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    # credential stuff
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    ### Basic Freebusy stuff ###
    # datetime object creation and manipulation for current time and an hour in the future
    now = datetime.datetime.utcnow()
    now_str = now.isoformat() + 'Z' # 'Z' indicates UTC time
    one_hour_future = now + datetime.timedelta(hours=1)
    one_hour_future_str = one_hour_future.isoformat() + 'Z'


    # creating HTTP Request body for Freebusy query method. Keep in mind this only checks the user's primary calendar;
    # we want to check ALL calendars of a given user, so we need to do some extra work with the API.
    req_body = {"timeMin":now_str, "timeMax":one_hour_future_str,"items":[{"id":"primary"}]}

    # step-by-step generation of Freebusy response. Normal code will be more succinct
    freeBusy = service.freebusy()
    freeBusyQuery = freeBusy.query(body=req_body)
    freeBusyResponse = freeBusyQuery.execute()
    ### END ###

    ### Extracting all calendars with a given user credentials ###
    # step-by-step generation of CalList response. Normal code will be more succinct
    calList = service.calendarList()
    calListRequest = calList.list()
    calListResponse = calListRequest.execute()
    for calendar_list_entry in calListResponse['items']:
        print(calendar_list_entry['id'])

    ### Retrying freebusy query with multiple calendars
    req_body = {"timeMin": now_str,
                "timeMax": one_hour_future_str,
                "items": [{"id": "ilctech.test@gmail.com"},
                          {"id":"204l1l7j7vb609nohtikek9ih8@group.calendar.google.com"}]}

    # step-by-step generation of Freebusy response. Normal code will be more succinct
    freeBusy = service.freebusy()
    freeBusyQuery = freeBusy.query(body=req_body)
    freeBusyResponse = freeBusyQuery.execute()
    calendars_structure = freeBusyResponse["calendars"]
    print(calendars_structure)
    for calendar in freeBusyResponse["calendars"]:
        print(calendar)
        print(calendars_structure[calendar]["busy"])
    # print(freeBusyResponse)


    # return
    # ayy lmao


    # print('Getting the upcoming 10 events')
    # events = service.events()
    # eventsQuery = events.list()
    #     calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
    #     orderBy='startTime').execute()

    # # print(eventsResult)

    # events = eventsResult.get('items', [])

    # # print(events)

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])


if __name__ == '__main__':
    main()
