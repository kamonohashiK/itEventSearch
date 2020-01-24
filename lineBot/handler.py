import os
import sys
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    logger.error('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    logger.error('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


def main(event, context):
    signature = event["headers"]["X-Line-Signature"]
    body = event["body"]
    ok_json = {"isBase64Encoded": False,
               "statusCode": 200,
               "headers": {},
               "body": ""}
    error_json = {"isBase64Encoded": False,
                  "statusCode": 403,
                  "headers": {},
                  "body": "Error"}

    @handler.add(MessageEvent, message=TextMessage)
    def message(line_event):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('itEvent')

        PREFECTURES = ['北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島', '茨城', '栃木', '群馬', '埼玉', '千葉', '東京', '神奈川', '新潟', '富山', '石川', '福井', '山梨', '長野', '岐阜', '静岡', '愛知', '三重', '滋賀', '京都', '大阪', '兵庫', '奈良', '和歌山', '鳥取', '島根', '岡山', '広島', '山口', '徳島', '香川', '愛媛', '高知', '福岡', '佐賀', '長崎', '熊本', '大分', '宮崎', '鹿児島', '沖縄']

        text = line_event.message.text
        events = []
        if text == "作者に連絡":
            event = "このbotについてお気づきの点がありましたら、作者のTwitterアカウントにリプライもしくはDMでお知らせください。\nhttps://twitter.com/platypus_k86"
            line_bot_api.reply_message(line_event.reply_token, TextSendMessage(text=event))
        elif text in PREFECTURES:
            events = table.scan(
                FilterExpression=Attr('pref').eq(text)
            )
        else:
            events = table.scan(
                FilterExpression=Attr('title').contains(text)
            )

        if events['Items']:
            event = ""
            count = 0
            for e in sorted(events['Items'], key=lambda x: datetime.strptime(x['datetime'], '%Y-%m-%d %H:%M:%S')):
                event += e['datetime'][:-3] + "(" + e['pref'] + ")" + "\n"
                event += e['title'] + "\n"
                event += e['url'] + "\n"
                event += "\n"
                count += 1

                if count == 9:
                    break
            line_bot_api.reply_message(line_event.reply_token, TextSendMessage(text=event))
        else:
            event = "ヒットしたイベントはありませんでした。"
            line_bot_api.reply_message(line_event.reply_token, TextSendMessage(text=event))

    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        logger.error("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            logger.error("  %s: %s" % (m.property, m.message))
        return error_json
    except InvalidSignatureError:
        return error_json

    return ok_json