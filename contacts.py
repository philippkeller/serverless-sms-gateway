import httplib2
import os
import datetime
from apiclient import discovery

from oauth2client import client

def birthday_today():
    """
    return list of strings of name (and birthyear) of people in
    my contacts list which have birthday today.
    """

    access_token = os.environ['GOOGLE_PEOPLE_ACCESS_TOKEN']
    credentials = client.AccessTokenCredentials(access_token, 'sms-proxy')
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('people', 'v1', http=http,
        discoveryServiceUrl='https://people.googleapis.com/$discovery/rest',
        cache_discovery=False)

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
