from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import pyttsx3
import speech_recognition as sr

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def send_data():
    # Replace this with your actual data or logic to fetch data
    data = {'message': 'Hello from Flask!'}
    print(data)
    return jsonify(data)

@app.route('/api/get', methods=['POST'])
def get_data():
    data = request.json  # Assuming the data is sent as JSON in the request body
    message = data.get('message', 'No message received')
    print('Received message:', message)

    # Perform any processing or return a response if needed
    response_data = {'status': 'Message received successfully'}
    return jsonify(response_data)

@app.route('/get_calendar_events', methods=['GET'])
def calendar_events():
    print("hello world")
    with open('static/example_events.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
