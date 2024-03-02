from flask import Flask, render_template, jsonify, request
from flask_cors import CORS


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

if __name__ == '__main__':
    app.run(debug=True)
