import json
from urllib import parse
import os

def sms_handler(event, context):
    import sms
    # gotten sms, at the moment just send the same sms back
    print(event)
    params = parse.parse_qs(event['body'])
    body = params['Body'][0]
    from_number = params['From'][0]
    sms.send(from_number, "testi--" + body)
