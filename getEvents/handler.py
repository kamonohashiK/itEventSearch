import json
import requests
import boto3

def hitConnpass(array, area):
    URL = "https://connpass.com/api/v1/event?keyword=" + area

    response = requests.get(URL)
    ary = response.json()['events']

    for a in ary:
        event = {
            'title': a['title'],
            'url': a['event_url'],
            'datetime': a['started_at'],
            'pref': area,
            'from': 'Connpass'
        }

        array.append(event)

def hitDoorkeeper(array, area):
    URL = "https://api.doorkeeper.jp/events?q=" + area

    response = requests.get(URL)
    ary = response.json()

    for a in ary:
        event = {
            'title': a['event']['title'],
            'url': a['event']['public_url'],
            'datetime': a['event']['starts_at'],
            'pref': area,
            'from': 'DoorKeeper'
        }

        array.append(event)

def hitAtnd(array):
    URL = "http://api.atnd.org/events/?format=json&count=100"

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

    db = boto3.resource('dynamodb')
    target = db.Table("eventSearchBot")
    num = target.get_item(Key = {'id': 1})
    number = num['Item']['number']

    PREFECTURES = ['北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島', '茨城', '栃木', '群馬', '埼玉', '千葉', '東京', '神奈川', '新潟', '富山', '石川', '福井', '山梨', '長野', '岐阜', '静岡', '愛知', '三重', '滋賀', '京都', '大阪', '兵庫', '奈良', '和歌山', '鳥取', '島根', '岡山', '広島', '山口', '徳島', '香川', '愛媛', '高知', '福岡', '佐賀', '長崎', '熊本', '大分', '宮崎', '鹿児島', '沖縄']

    hitConnpass(events, PREFECTURES[int(number)])
    hitDoorkeeper(events, PREFECTURES[int(number)])
    #hitAtnd(events)

    table = db.Table("Event")

    for e in events:
        table.put_item(
            Item={
                'title': e['title'],
                'url': e['url'],
                'datetime': e['datetime'],
                'pref': e['pref'],
                'from': e['from']
            }
        )

    nextNumber = number + 1
    if nextNumber == 47:
        nextNumber = 0

    target.put_item(
        Item={
            'id': 1,
            'number': nextNumber
        }
    )

    return True
