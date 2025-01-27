from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure maximum file size (e.g., 16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

API_ENDPOINT = "https://n8n-sgsh.onrender.com/webhook/scriba/scontrino"
API_AUTH = "prova"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Prepare the file for the API request
        files = {'file': (file.filename, file.stream, file.content_type)}
        headers = {'Authorization': API_AUTH}

        # Make the API request
        response = requests.post(API_ENDPOINT, headers=headers, files=files)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Return the API response
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))