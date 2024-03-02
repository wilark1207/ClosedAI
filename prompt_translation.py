import re
import json
from openai import OpenAI

client = OpenAI()

DESCRIPTIVE_PROMPT = 1
MODIFICATION_PROMPT = 2
INVALID_PROMPT = 3

prompt = "Add a lecture today between 3 and 5 pm"

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
            "start": {"dateTime": "2024-03-03T10:00:00Z", "timeZone": "UTC"},
            "end": {"dateTime": "2024-03-03T12:00:00Z", "timeZone": "UTC"},
            "reminders": {"useDefault": True},
        },
        {
            "summary": "Event 2",
            "location": "Event 2 location",
            "description": "Description of Event 2",
            "start": {"dateTime": "2024-03-03T14:00:00Z", "timeZone": "UTC"},
            "end": {"dateTime": "2024-03-03T16:00:00Z", "timeZone": "UTC"},
            "reminders": {"useDefault": True},
        },
    ],
}


def is_modif_or_description(prompt):
    result = (
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "Is this asking to read the calendar (type1) or is it asking to write on the calendar (type2) or if it is not relevant to calendars or time (type3), answer in this format: This is: Type(1 or 2 or 3 would go here) - "
                    + prompt,
                }
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
                        "content": "Your calendar is this json object - "
                        + json.dumps(calendar),
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
                    {
                        "role": "system",
                        "content": "The format of the calendar is this json object - "
                        + json.dumps(calendar),
                    },
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


def get_date_from_prompt(prompt):

    result = (
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                    + "Here I am referring to the range of dates based on today, I don't want an answer I only want the dates specified within that period. Return your answer in the format yyyy-mm-dd. Do not say anything else.",
                }
            ],
        )
        .choices[0]
        .message.content
    )

    return result


print(get_results(prompt, calendar))
