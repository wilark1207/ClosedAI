import datetime
import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# service = get_calendar_service()

# if get_prompt_type(prompt) == DESCRIPTIVE_PROMPT:
#     event_list = fetch_events(service, get_date_from_prompt(prompt))
#     return get_results(prompt, event_list) 

# elif get_prompt_type(prompt) == MODIFICATION_PROMPT:
#   return create_event(service, get_json_from_prompt(prompt))

def create_event(service, events_string):
  try:
    events_list = json.loads(events_string)

    for event in events_list:
        event = service.events().insert(calendarId='primary', body=event).execute()

    return 'The event(s) have been created successfully in your calendar'

  except HttpError as error:
    print(f"An error occurred: {error}")
    return 'f"An error occurred. Events could not be created: {error}"'



if __name__ == "__main__":
  string = '''
    [{
    "summary": "Meeting with Client",
    "start": {
    "dateTime": "2024-03-03T09:00:00",
    "timeZone": "Australia/Sydney"
    },
    "end": {
    "dateTime": "2024-03-03T10:00:00",
    "timeZone": "Australia/Sydney"
    }
    }]
    '''
  create_event(string)


