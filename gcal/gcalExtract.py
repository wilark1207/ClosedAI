import os.path
import requests
import datetime as dt
import datetime

from datetime import datetime, timedelta
import json

import pickle
import pytz
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    creds = None

    # token.pickle stores the user's access and refresh tokens, and is
    # automatically created when authorization flow completes for the firs time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service


#
# target date - ai
# today's date - variable
#
#
def fetch_events(service, year, month, day, range):

    tz = pytz.timezone("Australia/Sydney")

    timeMin = datetime(year, month, day, tzinfo=tz) - timedelta(days=range)
    timeMax = datetime(year, month, day, tzinfo=tz) + timedelta(days=range)

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=timeMin.isoformat(),
            timeMax=timeMax.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found. ")
    # for event in events:
    #     start = event["start"].get("dateTime", event["start"].get("date"))
    #     print(start, event["summary"])
    else:
        # events_data = json.loads(json.dumps(events, indent=2))
        # for event in events_data:
        #     print(event)

        # print(json.dumps(events, indent=2))
        return events_result
