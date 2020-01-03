import json
import requests
import boto3

def hitConnpass(array, area):
    URL = "https://connpass.com/api/v1/event?count=100&keyword=" + area

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
    URL = "https://api.doorkeeper.jp/events?page=100&prefecture=" + area
    # キーワードで検索する場合はパラメータqを使う

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

    PREFECTURES = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']

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
