import httplib2
import os
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# to get this initially working, follow
# https://developers.google.com/people/quickstart/python
# and store the client_secret.js into this projects directory
# then start this script with `python3 contacts.py` and
# authorize this app. The secret is then stored in
# people-api-secret.json
# 
# you can delete client_secret.js afterwards

SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'SMS Proxy'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def get_credentials():
    credential_path = os.path.join(SCRIPT_DIR, 'people-api-secret.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def birthday_today():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('people', 'v1', http=http,
        discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')

    results = service.people().connections().list(
            resourceName='people/me',
            pageSize=2000,
            personFields='names,birthdays').execute()
    connections = results.get('connections', [])
    today = datetime.date.today()
    res = []

    for person in connections:
        if 'birthdays' in person and 'names' in person and len(person['names']) > 0:
            birthday = person['birthdays'][0]['date']
            name = person['names'][0]['displayName']
            if birthday['month'] == today.month: # and birthday['day'] == today.day:
                if 'year' in birthday:
                    res.append("{}: {}".format(name, birthday['year']))
                else:
                    res.append("{}".format(name))
    return res

if __name__ == '__main__':
    print(birthday_today())