import json
import requests
import boto3
import re
import datetime

def main(event, context):
    events = []

    db = boto3.resource('dynamodb')
    target = db.Table("eventSearchBot")
    num = target.get_item(Key = {'id': 1})
    number = num['Item']['number']

    PREFECTURES = ['北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島', '茨城', '栃木', '群馬', '埼玉', '千葉', '東京', '神奈川', '新潟', '富山', '石川', '福井', '山梨', '長野', '岐阜', '静岡', '愛知', '三重', '滋賀', '京都', '大阪', '兵庫', '奈良', '和歌山', '鳥取', '島根', '岡山', '広島', '山口', '徳島', '香川', '愛媛', '高知', '福岡', '佐賀', '長崎', '熊本', '大分', '宮崎', '鹿児島', '沖縄']

    URL = "https://connpass.com/api/v1/event?count=100&keyword=" + PREFECTURES[int(number)]

    response = requests.get(URL)
    ary = response.json()['events']

    for a in ary:
        if a['address'] and PREFECTURES[int(number)] in a['address']:
            t = a['started_at'].replace("T", " ")
            time = re.sub(r'\+.*$', '', t)
            dt = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            ut = dt.timestamp()
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if string_to_datetime(now) < dt:
                event = {
                    'title': a['title'],
                    'url': a['event_url'],
                    'datetime': time,
                    'pref': PREFECTURES[int(number)],
                    'unixtime': int(ut),
                    'from': 'Connpass'
                }

                events.append(event)
    table = db.Table("itEvent")

    for e in events:
        table.put_item(
            Item={
                'title': e['title'],
                'url': e['url'],
                'datetime': e['datetime'],
                'unixtime': e['unixtime'],
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
            'number': nextNumber,
            'caption': 'Connpass'
        }
    )

    return True

def string_to_datetime(string):
    return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")