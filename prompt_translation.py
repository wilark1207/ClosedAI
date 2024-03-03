import re
import json
from openai import OpenAI
from datetime import date as d
from datetime import datetime, timedelta


client = OpenAI()

DESCRIPTIVE_PROMPT = 1
MODIFICATION_PROMPT = 2
INVALID_PROMPT = 3

prompt = "Am I busy tomorrow 2pm?"

calendar = {
    "summary": "My Calendar",
    "timeZone": "UTC",
    "description": "Description of my calendar",
    "colorId": 1,
    "backgroundColor": "#ffffff",
    "foregroundColor": "#000000",
    "selected": True,
    "hidden": False,
    "location": "Event location",
    "defaultReminders": [{"method": "popup", "minutes": 30}],
    "events": [
        {
            "summary": "Event 1",
            "location": "Event 1 location",
            "description": "Description of Event 1",
            "start": {
                "dateTime": "2024-03-03T10:00:00Z",
                "timeZone": "Australia/Sydney",
            },
            "end": {"dateTime": "2024-03-03T12:00:00Z", "timeZone": "Australia/Sydney"},
            "reminders": {"useDefault": True},
        },
        {
            "summary": "Event 2",
            "location": "Event 2 location",
            "description": "Description of Event 2",
            "start": {
                "dateTime": "2024-03-03T14:00:00Z",
                "timeZone": "Australia/Sydney",
            },
            "end": {"dateTime": "2024-03-03T16:00:00Z", "timeZone": "Australia/Sydney"},
            "reminders": {"useDefault": True},
        },
    ],
}

format = [
    {
        "summary": "Meeting with Client",
        "start": {"dateTime": "2024-03-03T09:00:00", "timeZone": "Australia/Sydney"},
        "end": {"dateTime": "2024-03-03T10:00:00", "timeZone": "Australia/Sydney"},
    },
]


def get_three_months_range(current_date):
    # Parse the input date string to a datetime object
    current_date = datetime.strptime(current_date, '%Y-%m-%d')

    # Calculate the date 6 months before the current date
    six_months_before = current_date - timedelta(days=3*30)

    # Calculate the date 6 months after the current date
    six_months_after = current_date + timedelta(days=3*30)

    # Return the results as a tuple
    return six_months_before.strftime('%Y-%m-%d'), six_months_after.strftime('%Y-%m-%d')

# Example usage:
current_date = datetime.now().strftime('%Y-%m-%d')
date = get_three_months_range(current_date)

def is_modif_or_description(prompt):
    result = (
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "When you get the input from the user. Is the user asking to read the calendar (type1) or is it asking to write on the calendar (type2) or if it is not relevant to calendars or time (type3),  answer in this format: This is: Type(1 or 2 or 3 would go here) Don't say anything else.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        .choices[0]
        .message.content
    )

    if re.search(str(DESCRIPTIVE_PROMPT), result) != None:
        return DESCRIPTIVE_PROMPT
    elif re.search(str(MODIFICATION_PROMPT), result) != None:
        return MODIFICATION_PROMPT
    return INVALID_PROMPT



def get_results(prompt, calendar):
    type = is_modif_or_description(prompt)
    print(type)
    result = None

    if type == DESCRIPTIVE_PROMPT:
        # he said put it in here
        result = (
            client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "This is the calendar data,"
                        + json.dumps(calendar)
                        + "You are to provide an answer to the user prompt according to this data",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            .choices[0]
            .message.content
        )
    elif type == MODIFICATION_PROMPT:
        result = (
            client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    # {
                    #     "role": "system",
                    #     "content": "The format of the calendar is this json object - "
                    #     + json.dumps(calendar),
                    # },
                    {
                        "role": "user",
                        "content": prompt
                        + "\nGive the modifications only as a google calendar api json object",
                    },
                ],
            )
            .choices[0]
            .message.content
        )

    return result


def description_reply():
    result = (
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Your calendar is this json object - "
                    + json.dumps(calendar),
                },
                {"role": "user", "content": prompt},
            ],
        )
        .choices[0]
        .message.content
    )

#here the user will be referring to the range of dates based on today, I don't want an answer I only want the dates specified within that period. If the date is only one say that date is X, then return the dates X -1 and X + 1 in one line separated by space. Otherwise Return your answer in the format yyyy-mm-dd yyyy-mm-dd. Do not say anything else.

def get_date_from_prompt(prompt):

    todays_date = d.today()

    result = (
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that helps summarise conversations from text based on the transcription of these texts and collected specified range of dates. Don't say anything but the dates in the response. Today's date is "
                    + str(todays_date) + "Example: [The current date in this example is 2024-03-02, and the day of the week is Sunday], Customer: Good morning, I want to know what my schedule looks like for the coming tuesday"
                    + " Agent: 2024-03-04 2024-03-06"
                    + " It is MANDATORY that the following structure of dates are TWO dates in the format: 'yyyy-mm-dd yyyy-mm-dd'"
                    + "If the prompt refers to only one date, then given X is that date, only return the dates X - 1 and X + 1 in the format that I specified."
                    + "If the user mentions a day of the week equal to monday, consider money of the following week. IF THE USER MENTIONS THE DAY OF THE WEEK, FIRST"
                    + "CALCULATE THE DATE FOR THAT DAY BASED ON THE CURRENT DATE" + str(todays_date) + ". All mentioned dates are independent, so for each, always compare with the current date.",
                },

                {"role": "user", "content": prompt + "Todays date is " + str(todays_date)},
            ],
        )
        .choices[0]
        .message.content
    )

    return result

def get_json_from_prompt(prompt):

    result = (
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "If there are multiple events, I want you to return an array of json objects. Otherwise, if it is a single object, just return the single json object. I want the timezone to be "
                    + "Australia/Sydney"
                    + ". Here is a format i want a single json to be in: "
                    + json.dumps(format)
                    + "In arrays you would have multiple of these.  I want you to return these json objects as text, and not a json file.  Don't say anything else other than the json object in text format, don't have it in code files",
                },
                {"role": "user", "content": prompt},
            ],
        )
        .choices[0]
        .message.content
    )

    return result
