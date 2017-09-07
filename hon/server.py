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

        if messageText == ("コマンド"):
            state = "no need analyze"
            command_message = "みしまくんはね、weekly reportや文章を入力すると、ポジティブ度を教えてあげるよ。\n" \
                                + "「ポジティブランキング 2017/03」　と打つとその月のポジティブな文章を教えるよ。 \n" \
                                + "「ネガティブランキング 2017/03」　と打つとその月のネガティブな文章を教えるよ。"

            send_message(companyId, groupId, command_message)

        elif messageText.find('<< WEEKLY REPORT >>') >= 0:  # WEEKLY REPORT
            preprocessed_text = preprocess.preprocess(messageText) #テキストをAIに読みやすいようにする工程
            state = "WR"

        elif messageText.count("。") >= 2:  # WEEKLY REPORTでない長文
            preprocessed_text = preprocess.preprocess(messageText) #テキストをAIに読みやすいようにする工程
            state = "long message"

        elif messageText.find('週報') >= 0 and messageText.find('判断') >= 0:
            send_message(companyId, groupId, "判断したい週報を入力してください！")
            state = "no need analyze"

        elif messageText.find('ポジティブランキング') >= 0:
            month = messageText[11:18]
            month = month.split('/')
            print(month)
            dic = analyze.open_old_WR('staff_wr_sample')
            print(dic)
            state = "max_ranking"


        else:
            state = "short message"
            if messageText.find("。") >= 0:
                preprocessed_text = preprocess.preprocess(messageText)
            else:
                preprocessed_text = messageText


        if state != "no need analyze":
            analyzed_dict = analyze.analyze(preprocessed_text)
            analyze.save_fig(analyzed_dict['score_list'])

            if state == "WR":  # WEEKLY REPORTだった場合のメッセージリターン
                return_message = set_message_WR(analyzed_dict)  # メッセージを整形

                send_message(companyId, groupId, return_message[0])  # メッセージを送信
                send_message(companyId, groupId, return_message[1])
                send_message(companyId, groupId, return_message[2])

            elif state == "long message":  # WEEKLY REPORTじゃない長文
                return_message = set_message_LG(analyzed_dict)

                send_message(companyId, groupId, return_message[0])  # メッセージを送信
                send_message(companyId, groupId, return_message[1])
                send_message(companyId, groupId, return_message[2])

            elif state == "short message":
                return_message = set_message_SH(analyzed_dict)

                send_message(companyId, groupId, return_message[0])

            else:
                send_message(companyId, groupId,"「" + messageText + "」は受付ませんでした。")
                print("! MESSAGE REJECTED")
                state = "message rejected"


        #if state != "message rejected":
        if state != "short message" and state != "no need analyze":
            send_file(companyId, groupId, "./fig_histgram.png")
        print(state)
        print(messageText.find('\n'),messageText.find('。'))
        print("MESSAGES SENDED")  # log
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

    file_name = os.path.basename(file_path)

    image = open(file_path, "rb")

    files = {

        'file': (file_name, image, 'image/png')

    }

    data = {

        'fileName': file_name

    }

    res = requests.post(url, headers=headers, files=files, data=data)


def get_score(score):
    score = score + 1  # 0-2
    score = score * 50  # 0-100
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

    message.append("ウィークリーレポートの合計は、" + str(totalvalue) + "点でした\n" \
                    "来週もがんばりましょう！！")

    return message


def set_message_LG(analyzed_value):
    maxvalue = get_score(analyzed_value['max']['score'])
    minvalue = get_score(analyzed_value['min']['score'])
    totalvalue = get_score(analyzed_value['total'])

    message = []
    message.append("とってもポジティブな文章は、\n「" + analyzed_value['max']['sentence'] + \
                   "」\nで、" + str(maxvalue) + "点でした！\n")

    message.append("すっごくネガティブな文章は、\n「" + analyzed_value['min']['sentence'] + \
                   "」\nで、" + str(minvalue) + "点でした><\n")

    message.append("合計は、" + str(totalvalue) + "点でした\n" \
                   "来週もがんばりましょう！！")

    return message

def set_message_SH(analyzed_value):
    totalvalue = get_score(analyzed_value['total'])

    message = []
    message.append("あなたが送った文章は、" + str(totalvalue) + "点でした！\n")

    return message


"""
message = 'RESULT' + \
'\nMAX = ' + str(analyzed_value['max']['score']) + \
'\nMIN = ' + str(analyzed_value['min']['score']) + \
'\nMID = ' + str(analyzed_value['mid']['score']) + \
'\nMAGNITUDE = ' + str(analyzed_value['magnitude']) + \
'\nTOTAL = ' + str(analyzed_value['total'])
"""


def dammy():
    dic = {'max': {'score': 0.8, 'sentense':"あｆｐふぁｗｋぱ"},
           'min': {'score': -0.4,'sentense':"うぃふぉあえふぉうぇ"},
           'sum': 14,
           'ave': -0.5,
           'mid': {'score': 0},
           'magnitude': 11,
           'total': -4,
           'max_list': {'max_score_list': [0.9, 0.8, 0.8],
                        'max_sentence_list': ['I am Happy', 'Hello good morning', 'Happy New Year']
                        }
           }

    return dic


if __name__ == '__main__':
    app.run(host='', port=80, debug=True)
