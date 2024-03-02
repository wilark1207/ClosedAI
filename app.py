from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
#import prompt_translation
import json
import pyttsx3
import speech_recognition as sr
import database

# text to speech
def textToSpeech(text, gender='Male'):
    """
    Convert text to speech
    :param text: text
    :param gender: gender
    :return: None
    """
    voice_dict = {'Male': 0, 'Female': 1}
    code = voice_dict[gender]
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)
    engine.setProperty('volume', 0.8)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)

    engine.say(text)
    engine.runAndWait()

app = Flask(__name__)
CORS(app)

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

def parse(prompt):
    database.add_message("AI", prompt + ": This request is currently unavailable.")

@app.route('/')
def home():
    reply = database.get_messages()
    return render_template('index.html', reply=reply)

@app.route('/api/messages', methods=['GET'])
def send_messages():
    # Replace this with your actual data or logic to fetch data
    data = database.get_messages()
    print(data)
    return jsonify(data)

@app.route('/api/data', methods=['GET'])
def send_data():
    # Replace this with your actual data or logic to fetch data
    data = {'message': 'Hello from Flask!'}
    print(data)
    return jsonify(data)

@app.route('/api/get', methods=['POST'])
def get_data():
    data = request.json
    message = data.get('msg')  # Use 'input' instead of 'msg'
    print('Received message:', message)

    try:
        split_input = message.split(":\"")
        prompt = split_input[1][:-2]
        print(prompt)
        database.add_message("USER", prompt)
        parse(prompt)
    except:
        #Flashs
        return "Invalid message"

    # Perform any processing or return a response if needed
    response_data = {'status': message}
    return prompt 


@app.route('/get_calendar_events', methods=['GET'])
def calendar_events():
    print("hello world")
    with open('static/example_events.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
    