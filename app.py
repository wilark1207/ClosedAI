from flask import Flask, jsonify, render_template, request
import pyttsx3
import speech_recognition as sr
import json

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

@app.route('/')
def home():
    with open('static/example_events.json') as json_file:
        data = json.load(json_file)
    print(data)
    # Pass the JSON data to the template
    return render_template('index.html', myjson=data)

"""
Example route to get the text after recording mic successfully
@app.route('/receive_text', methods=['POST'])
def receive_text():
    data = request.json
    text = data.get('text', '')
    gender = data.get('gender', 'Male')  # Default gender to Male if not specified
    print(f"Received text: {text}")
    # Test Text to speech
    textToSpeech(text, gender)
    return jsonify({"message": "Text received and converted to speech successfully!"})
"""


if __name__ == '__main__':
    app.run(debug=True)
