import os.path
import requests
import datetime as dt
import datetime

from datetime import datetime, timedelta
import json
import pytz
from zoneinfo import ZoneInfo

# from prompt_translation import get_results

import pickle
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
def fetch_events(service, dates):

    print(f"Dates fed into fetch events function are: {dates}")

    tz = pytz.timezone("Australia/Sydney")

    date_parts = dates.split()


    date1 = date_parts[0].split("-")
    date1Year, date1Month, date1Day = map(int, date1)

    date2 = date_parts[1].split("-")
    date2Year, date2Month, date2Day = map(int, date2)

    timeMin = datetime(date1Year, date1Month, date1Day, tzinfo=tz)
    timeMax = datetime(date2Year, date2Month, date2Day, tzinfo=tz)

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
    event_data = []

    for event in events:
        summary = event.get("summary", "No summary available")
        start_time = event["start"].get(
            "dateTime", event["start"].get("date", "No start time available")
        )
        end_time = event["end"].get(
            "dateTime", event["end"].get("date", "No end time available")
        )
        location = event.get("location", "No location available")
        description = event.get("description", "No description available")
        event_info = {
            "summary": summary,
            "start_time": start_time,
            "end_time": end_time,
            "location": location,
            "description": description,
        }
        event_data.append(event_info)

    return event_data


service = get_calendar_service()
#print(fetch_events(service, "2024-02-29 2024-03-02"))

