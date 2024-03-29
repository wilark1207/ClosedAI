from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
#import prompt_translation
import database
import json
import gcal.gcalExtract as gcal
import prompt_translation as pt
from datetime import date
from datetime import datetime, timedelta
import create_event as ce

import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path

app = Flask(__name__)
CORS(app)

DESCRIPTIVE_PROMPT = 1
MODIFICATION_PROMPT = 2

conn = sqlite3.connect('messages.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author VARCHAR(20) NOT NULL,
        content TEXT NOT NULL
    )
''')
#cursor.execute('INSERT INTO messages (author, content) VALUES (?, ?)', ('AI', 'How can I assist you today?'))
conn.commit()
conn.close()


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_service():
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

def parse(prompt):
    current_date = datetime.now().strftime('%Y-%m-%d')
    service = get_service()

    if pt.is_modif_or_description(prompt) == DESCRIPTIVE_PROMPT:
        print("1")
        event_list = gcal.fetch_events(service, pt.get_date_from_prompt(prompt))
        database.add_message("AI", pt.get_results(prompt, event_list))
        return pt.get_results(prompt, event_list)
    elif pt.is_modif_or_description(prompt) == MODIFICATION_PROMPT:
        print("2")
        database.add_message("AI", ce.create_event(service, pt.get_json_from_prompt(prompt)))
        print(pt.get_json_from_prompt(prompt))
        return ce.create_event(service, pt.get_json_from_prompt(prompt))


@app.route('/')
def home():
    with open('static/example_events.json') as json_file:
        data = json.load(json_file)
    print(data)
    # Pass the JSON data to the template
    reply = database.get_messages()
    return render_template('index.html', reply=reply)

@app.route('/api/messages', methods=['GET'])
def send_messages():
    # Replace this with your actual data or logic to fetch data
    data = database.get_messages()
    
    return jsonify(data)

@app.route('/api/data', methods=['GET'])
def send_data():
    # Replace this with your actual data or logic to fetch data
    data = {'message': 'Hello from Flask!'}
    return jsonify(data)

@app.route('/api/get', methods=['POST'])
def get_data():
    data = request.json
    message = data.get('msg')
    # Pattern to extract text within {"input":"HERE"}
    if not message:
        return jsonify({"error": "Message is required"}), 400

    print('Received message:', message)

    # Assuming database.add_message() and parse() are valid operations:
    try:
        split_input = message.split(":\"")
        prompt = split_input[1][:-2]
        database.add_message("USER", prompt)
        response = parse(message)  # Assuming parse() returns something you want to send back
        return jsonify({"response": response}), 200
    except Exception as e:  # Catch any exception and return an error
        return jsonify({"error": str(e)}), 500

@app.route('/get_calendar_events', methods=['GET'])
def calendar_events():
    #print("hello world")
    with open('static/example_events.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
    