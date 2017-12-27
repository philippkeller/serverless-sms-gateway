import json
from urllib import parse
import os

def sms_handler(event, context):
    import sms
    # gotten sms, at the moment just send the same sms back
    params = parse.parse_qs(event['body'])
    body = params['Body'][0]
    from_number = params['From'][0]
    sms.send(from_number, "testi--" + body)

def birthday_handler(event, context):
    import contacts
    res = contacts.birthday_today()
    if len(res) > 0:
        import sms
        body = "\n".join(res)
        twilio_number = os.environ['TWILIO_NOTIFICATIONS']
        sms.send(twilio_number, body)