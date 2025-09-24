from flask import Flask, request, jsonify, render_template, redirect, url_for
from wtforms import Form, StringField, validators, SubmitField
import requests
import os
from requests.auth import HTTPBasicAuth as htt
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
class InputForm(Form):
    phone_number = StringField('Phone Number', [validators.DataRequired(), validators.Length(min=10, max=15)])
    text_message = StringField('Text Message', [validators.DataRequired(), validators.Length(min=1, max=160)])
    submit = SubmitField('Call Me!')



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/call', methods=['GET', 'POST'])
def call():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        phone_number = form.phone_number.data
        text_message = form.text_message.data

        def strip_code(message):
            for word in message.split():
                if word.isdigit() and len(word) < 6:
                    return word 



        username = os.getenv("TELESIGN_ID")
        password = os.getenv("TELESIGN_KEY")

        url = "https://rest-ww.telesign.com/v1/verify/call"

        payload = { "language": "en-US", 
                    "verify_code": strip_code(text_message), 
                    "phone_number": phone_number, 
                    "ucid": "BACS" }           
        

        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }


        response = requests.post(url, data=payload, headers=headers, auth=htt(username, password))

        print(response.text)
        return redirect(url_for('home'))
    return render_template('call.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)