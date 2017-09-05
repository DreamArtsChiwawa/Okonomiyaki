#!/usr/bin/python

import os

import json

import requests

from flask import Flask, request

import sys

sys.path.append('../miyagishi/')
import analyzeSentiment

app = Flask(__name__)

env = os.environ


@app.route('/', methods=['GET'])
def helloPage():
    return "Hello python bot."


@app.route('/messages', methods=['POST'])
def messages():
    if is_request_valid(request):

        body = request.get_json(silent=True)

        companyId = body['companyId']

        msgObj = body['message']

        groupId = msgObj['groupId']

        messageText = msgObj['text']

        userName = msgObj['createdUserName']

        if messageText in '週報' or messageText in "ウィークリーレポート":
            send_message(companyId, groupId, "判断したい週報を!")
            if messageText in ["判断"]:
                send_message(companyId, groupId, "判断したい週報を入力してください！")

        if 1 == 1:  # messageText in ["<< WEEKLY REPORT >>"]:
            # AIをここを実行して値を取得する
            weeklyreport = messageText
            # value = analyzeSentiment.analyze(weeklyreport)
            value = {'max': {'score': 0.21, 'sent': "今日はぽかぽか陽気でした．"}, 'min': {'score': -0.7, 'sent': "神がはねてて最悪でした．"},
                     'res': -0.4}

            maxvalue = get_value(value['max']['score'])
            minvalue = get_value(value['min']['score'])
            # maxvalue = (value['max']['score'])
            # minvalue = (value['min']['score'])
            # print(maxvalue)
            # print(minvalue)
            value_res = get_value(value['res'])

            send_message(companyId, groupId, "とってもポジティブな文章は、「" + value['max']['sent'] + "」で、" + str(
                int(maxvalue)) + "点でした！\n" + "すっごくネガティブな文章は、「" + value['min']['sent'] + "」で、" + str(
                int(minvalue)) + "点でした！\n" + "ウィークリーレポートの総計は、" + str(int(value_res)) + "点でした")

        print("OK!")
        return "OK"

    else:

        return "Request is not valid."


def get_value(score):
    value = score + 1
    value = value * 50
    return (value)


# Check if token is valid.

def is_request_valid(request):
    validationToken = env['CHIWAWA_VALIDATION_TOKEN']

    requestToken = request.headers['X-Chiwawa-Webhook-Token']

    return validationToken == requestToken


# Send message to Chiwawa server

def send_message(companyId, groupId, message):
    url = 'https://{0}.chiwawa.one/api/public/v1/groups/{1}/messages'.format(companyId, groupId)

    headers = {

        'Content-Type': 'application/json',

        'X-Chiwawa-API-Token': env['CHIWAWA_API_TOKEN']

    }

    content = {

        'text': message

    }

    requests.post(url, headers=headers, data=json.dumps(content))


if __name__ == '__main__':
    app.run(host='', port=80, debug=True)
