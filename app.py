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
    data = request.json
    message = data.get('msg')  # Use 'input' instead of 'msg'
    print('Received message:', message)

    try:
        split_input = message.split(":\"")
        prompt = split_input[1][:-2]
        print(prompt)
    except:
        #Flash
        return "Invalid message"

    # Perform any processing or return a response if needed
    response_data = {'status': message}
    return jsonify(response_data)   

if __name__ == '__main__':
    app.run(debug=True)
    