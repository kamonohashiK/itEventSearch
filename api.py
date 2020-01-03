# coding:utf-8
import requests
import json

# TODO: 開始時間のフォーマット整理
def hitConnpass(query):
    URL = "https://connpass.com/api/v1/event?keyword=" + query

    response = requests.get(URL)
    ary = response.json()['events']

    print('Doorkeeper')
    for a in ary:
        print(a['title'])
        print(a['event_url'])
        print(a['started_at'])
        print(a['address'])

def hitDoorkeeper(query):
    URL = "https://api.doorkeeper.jp/events?prefecture=" + query
    # キーワードで検索する場合はパラメータqを使う

    response = requests.get(URL)
    ary = response.json()

    print('DoorKeeper')
    for a in ary:
        print(a['event']['title'])
        print(a['event']['starts_at'])
        print(a['event']['public_url'])
        print(a['event']['address'])

def hitAtnd(query):
    URL = "http://api.atnd.org/events/?format=json&keyword=" + query
    # キーワードで検索する場合はパラメータqを使う

    response = requests.get(URL)
    ary = response.json()['events']

    #APIのレスポンス時点で過去イベント拾ってきちゃう　めんどくせえ
    print('Atnd')
    for a in ary:
        print(a['event']['title'])
        print(a['event']['event_url'])
        print(a['event']['started_at'])
        print(a['event']['address'])

hitConnpass('愛媛')
hitDoorkeeper('ehime')
hitAtnd('愛媛')