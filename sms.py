from twilio.rest import Client
import os

def send(from_number, to_number, body):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token  = os.environ['TWILIO_AUTH_TOKEN']

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=from_number, 
        from_=to_number,
        body=body)
