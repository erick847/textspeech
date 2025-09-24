import requests

url = "https://rest-ww.telesign.com/v1/verify/call"

payload = { "language": "en-US", 
            "verify_code": "1234", 
            "phone_number": "+255696606112", 
            "ucid": "BACS" }           
 

headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "authorization": "Basic OUQwNDBEN0EtQThCNC00RkFCLUIwQjItM0ZFOEJDODVBQTRFOkNMaXBsVStNL0FZdHZGTC9ncWtRalp0aWV3Tk9vUFBMbnI5KzF3R1hpOEp0OVZ0RHlCcDl4bHZUN2Q1K3dwVGFFbTQ2YlFHVlN2elRBZGpjVG9NcnFnPT0="
}

response = requests.post(url, data=payload, headers=headers)

print(response.text)