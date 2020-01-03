import json
import requests

def hitConnpass(array):
    URL = "https://connpass.com/api/v1/event"

    response = requests.get(URL)
    ary = response.json()['events']

    for a in ary:
        event = {
            'title': a['title'],
            'url': a['event_url'],
            'datetime': a['started_at'],
            'pref': a['address'],
            'from': 'Connpass'
        }

        array.append(event)

def hitDoorkeeper(array):
    URL = "https://api.doorkeeper.jp/events"
    # キーワードで検索する場合はパラメータqを使う

    response = requests.get(URL)
    ary = response.json()

    for a in ary:
        event = {
            'title': a['event']['title'],
            'url': a['event']['public_url'],
            'datetime': a['event']['starts_at'],
            'pref': a['event']['address'],
            'from': 'DoorKeeper'
        }

        array.append(event)

def hitAtnd(array):
    URL = "http://api.atnd.org/events/?format=json"

    response = requests.get(URL)
    ary = response.json()['events']

    for a in ary:
        event = {
            'title': a['event']['title'],
            'url': a['event']['event_url'],
            'datetime': a['event']['started_at'],
            'pref': a['event']['address'],
            'from': 'Atnd'
        }

        array.append(event)


def main(event, context):
    events = []

    hitConnpass(events)
    hitDoorkeeper(events)
    hitAtnd(events)

    return events
