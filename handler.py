import json

def sms(event, context):
    from twilio.rest import Client
    from urllib import parse
    import os
    
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token  = os.environ['TWILIO_AUTH_TOKEN']
    to = os.environ['TWILIO_TO']
    valid_from = [t.strip() for t in os.environ['TWILIO_VALID_FROM'].split(",")]
    print(valid_from)

    params = parse.parse_qs(event['body'])
    body = params['Body'][0]
    from_number = params['From'][0]

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=from_number, 
        from_=to,
        body="Got body {}".format(body))
