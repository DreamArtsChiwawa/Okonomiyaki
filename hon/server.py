import os
import json
import requests
from flask import Flask, request

import analyze
import preprocess

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

        state = "default"

        if messageText.find('週報') >= 0 and messageText.find('判断') >= 0:
            send_message(companyId, groupId,"判断したい週報を入力してください！")
            state = "no need analyze"




        if messageText.find('<< WEEKLY REPORT >>') >= 0: # WEEKLY REPORT
            preprocessed_text = preprocess.preprocess(messageText) #テキストをAIに読みやすいようにする工程
            state = "WR"
        elif messageText.find('\n') >= 1: # WEEKLY REPORTでない長文
            preprocessed_text = messageText
            state = "long message"
        else: # 短文
            preprocessed_text = messageText
            state = "short message"

        if state == "WR": # WEEKLY REPORTだった場合のメッセージリターン
            value = analyze.analyze(preprocessed_text)
            #value = dammy() #ダミーの辞書を生成
            return_message = set_message_WR(value) #メッセージを整形

            send_message(companyId, groupId, return_message[0]) #メッセージを送信
            send_message(companyId, groupId, return_message[1])
            send_message(companyId, groupId, return_message[2])

        send_message(companyId, groupId, "みしまくんは写真を送ることに成功しましたか？")
        send_file(companyId, groupId, "ori.png")
        print("MESSEAGES SENDED") #log

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


# Send file to Chiwawa server
def send_file(companyId, groupId, file_path):

    url = 'https://{0}.chiwawa.one/api/public/v1/groups/{1}/files'.format(companyId, groupId)

    headers = {

        'X-Chiwawa-API-Token': env['CHIWAWA_API_TOKEN']

    }

    file_name = os.path.basename(faile_path)
    
    image = open(file_path,"rb")

    files = {

        'file': (file_name,image,'image/png')

    }

    data = {

	'fileName':file_name

    }

    res = requests.post(url, headers=headers, files=files, data=data)


def get_score(score):
    score = score + 1 # 0-2
    score = score * 50 # 0-100
    return int(score)

def set_message_WR(analyzed_value):

    maxvalue = get_score(analyzed_value['max']['score'])
    minvalue = get_score(analyzed_value['min']['score'])
    totalvalue = get_score(analyzed_value['total'])

    message = []
    message.append("とってもポジティブな文章は、\n「" + analyzed_value['max']['sentence'] + \
                "」\nで、" + str(maxvalue) + "点でした！\n")


    message.append("すっごくネガティブな文章は、\n「" + analyzed_value['min']['sentence'] + \
                "」\nで、" + str(minvalue) + "点でした><\n")

    message.append("ウィークリーレポートの総計は、" + str(totalvalue) + "点でした\n" \
                "来週もがんばりましょう！！")

    """
    message = 'RESULT' + \
              '\nMAX = ' + str(analyzed_value['max']['score']) + \
              '\nMIN = ' + str(analyzed_value['min']['score']) + \
              '\nMID = ' + str(analyzed_value['mid']['score']) + \
              '\nMAGNITUDE = ' + str(analyzed_value['magnitude']) + \
              '\nTOTAL = ' + str(analyzed_value['total'])
    """
    return message
"""
def dammy():
    dic = {'max': {'score': 0.8, 'sentense':"あｆｐふぁｗｋぱ"},
           'min': {'score': -0.4,'sentense':"うぃふぉあえふぉうぇ"},
           'sum': 14,
           'ave': -0.5,
           'mid': {'score': 0},
           'magnitude': 11,
           'total': -4}

    return dic
"""

if __name__ == '__main__':
    app.run(host='', port=80, debug=True)
