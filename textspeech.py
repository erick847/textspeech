from flask import Flask, request, jsonify, render_template, redirect, url_for
from wtforms import Form, StringField, validators, SubmitField
import requests
import os
from requests.auth import HTTPBasicAuth as htt
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Define the form using WTForms
class InputForm(Form):
    phone_number = StringField('Phone Number', [validators.DataRequired(), validators.Length(min=10, max=15)])
    text_message = StringField('Text Message', [validators.DataRequired(), validators.Length(min=1, max=160)])
    submit = SubmitField('Call Me!')



@app.route('/')
def home():
    return render_template('index.html')

# Define the route for the form
@app.route('/call', methods=['GET', 'POST'])
def call():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        phone_number = form.phone_number.data
        text_message = form.text_message.data

# strip out code from message
        def strip_code(message):
            for word in message.split():
                if word.isdigit() and 3 <= len(word) <= 5:
                    return word 

# Get TeleSign credentials from environment variables
        username_call = os.getenv("TELESIGN_ID")
        password_call = os.getenv("TELESIGN_KEY")

        username_sms = os.getenv("SMS_API_KEY")
        password_sms = os.getenv("SMS_API_SECRET")

        telesign_url = "https://rest-ww.telesign.com/v1/verify/call"
        beem_sms_url = "https://apisms.beem.africa/v1/send"

# Prepare the payload for the API request
        payload_call = { "language": "en-US", 
                    "verify_code": strip_code(text_message), 
                    "phone_number": phone_number, 
                    "ucid": "BACS" }           
        

        headers_call = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }

        payload_sms = {
            "source_addr": "BEEMERS",
            "schedule_time": "",
            "encoding": "0",
            "message": text_message,
            "recipients": [
                {
                    "recipient_id": 1,
                    "dest_addr": phone_number
                }
            ]
        }

        headers_sms = {
            "accept": "application/json",
            "content-type": "application/json"
        }

# Make the API request to TeleSign to call the user if there is a code in the message, otherwise send SMS via Beem API
        def call_user():
            response_call = requests.post(telesign_url, data=payload_call, headers=headers_call, auth=htt(username_call, password_call))
            print(response_call.text)
        
        def send_sms():
            response_sms = requests.post(beem_sms_url, json=payload_sms, headers=headers_sms, auth=htt(username_sms, password_sms))
            print(response_sms.text)
            

        if strip_code(text_message):
            call_user()
        else:
            send_sms()     
        

# Redirect to home after submission

        return redirect(url_for('home'))
    return render_template('call.html', form=form)

# modify the function to send SMS if call is not picked or there is no code in the message


if __name__ == '__main__':
    app.run(debug=True)