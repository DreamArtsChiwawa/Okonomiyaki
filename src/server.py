#!/usr/bin/python
import os
import json
import requests
from flask import Flask, request

import analyze

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

        print(messageText)

        value = analyze.analyze(messageText)

        return_message = set_message(value)

        send_message(companyId, groupId, return_message)

        print("OK!")

        return "OK"

    else:

        return "Request is not valid."


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


def set_message(analyzed_value):
    message = 'RESULT' + \
              '\nMAX = ' + str(analyzed_value['max']['score']) + \
              '\nMIN = ' + str(analyzed_value['min']['score']) + \
              '\nMID = ' + str(analyzed_value['mid']['score']) + \
              '\nMAGNITUDE = ' + str(analyzed_value['magnitude']) + \
              '\nTOTAL = ' + str(analyzed_value['max'])

    return message


if __name__ == '__main__':
    app.run(host='', port=80, debug=True)
