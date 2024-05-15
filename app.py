from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gravatar', methods=['POST'])
def gravatar():
    email = request.form.get('email')

    if email:
        # Get Gravatar JSON response
        gravatar_data = hash_email(email)

        # Parse relevant fields from JSON
        username = parse_json(gravatar_data, 'preferredUsername')
        display_name = parse_json(gravatar_data, 'displayName')
        about_me = parse_json(gravatar_data, 'aboutMe')
        profile_url = parse_json(gravatar_data, 'profileUrl')

        return render_template('gravatar.html', username=username, display_name=display_name, about_me=about_me, profile_url=profile_url)
    else:
        return "Email not provided"



# gravatar.py

import requests
import hashlib
import json

def hash_email(email):
    md5_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()

    url = f'https://en.gravatar.com/{md5_hash}.json'
    response = requests.get(url)

    return response.json()

def gravatar_email(email):
    md5_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()

    url = f'https://en.gravatar.com/{md5_hash}.json'
    response = requests.get(url)

    checker = response.text

    text = '"User not found"'

    if text in checker:
        return f'false'
    else:
        return f'true'

def parse_json(json_response, field):
    # Check if the input is a non-empty string and parse it
    if isinstance(json_response, str) and json_response.strip():
        try:
            json_response = json.loads(json_response)
        except json.JSONDecodeError:
            return None

    try:
        entry = json_response["entry"][0]
        return entry[field] if field in entry else None
    except (KeyError, IndexError):
        return None
    


if __name__ == '__main__':
    app.run(debug=True)
