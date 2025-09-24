import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("TELESIGN_ID")
password = os.getenv("TELESIGN_KEY")

url = "https://rest-ww.telesign.com/v1/verify/call"

payload = { "language": "en-US", 
            "verify_code": "1234", 
            "phone_number": "+255684467957", 
            "ucid": "BACS" }           
 

headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=payload, headers=headers, auth=HTTPBasicAuth(username, password))

print(response.text)