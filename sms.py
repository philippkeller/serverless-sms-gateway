from twilio.rest import Client
import os

def send(to_number, body):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token  = os.environ['TWILIO_AUTH_TOKEN']
    twilio_number = os.environ['TWILIO_TO']

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=to_number, 
        from_=twilio_number,
        body=body)
