import numpy as np
import matplotlib.pyplot as plt
import sys
from google.cloud import language
from datetime import datetime


def analyze(text):
    """Run a sentiment analysis request on text within a passed filename."""
    language_client = language.Client()

    print(text)

    # review_file = head.get_text(text)
    review_file = text.replace('¥n', '\n')    # 改行文字の置き換え
    text_list = review_file.split("\n")             # 改行文字で分かち書き
    # print(review_file)
    # print(text_list)
    # with open(movie_review_filename, 'r') as review_file:
    # Instantiates a plain text document.
    # document = language_client.document_from_html(review_file)
    # print(type(text))
    # text = text.encode().decode('utf-8')
    # print(text)

    document = language_client.document_from_html(text)

    annotations = document.annotate_text(include_sentiment=True,
                                         include_syntax=False,
                                         include_entities=False)

    value_dict = set_dict(annotations, text_list)

    return value_dict


def set_dict(annotations, text_list):
    score = annotations.sentiment.score
    magnitude = annotations.sentiment.magnitude
    score_list = []

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}.The sentence is "{}"\n'.format(
            index, sentence_sentiment, text_list[index]))
        score_list.append(sentence_sentiment)

    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))

    sum_score = sum(score_list)
    ave_score = sum_score / len(score_list)
    max_score = max(score_list)
    min_score = min(score_list)
    mid_score = np.median(score_list)
    total_score = score

    print(score_list)

    n, bins, patch = plt.hist(score_list, bins=np.arange(-1.0, 1.01, 0.1))  # 度数分布表の取得   
    #plt.savefig("fig_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".png") # ヒストグラムをファイルに出力
    plt.savefig("fig_histgram.eps")

    # print('total score is {}'.format(sum_score))
    # print('average score is {}'.format(ave_score))
    # print('max score is {}.The Sentence is ({})'.format(max_score, text_list[score_list.index(max_score)]))
    # print('min score is {}'.format(min_score))
    # print('center score is {}'.format(center_score))

    dic = {'max': {'score': max_score, 'sentence': text_list[score_list.index(max_score)]},
           'min': {'score': min_score, 'sentence': text_list[score_list.index(min_score)]},
           'sum': sum_score,
           'ave': ave_score,
           'mid': {'score': mid_score},
           'magnitude': magnitude,
           'total': total_score}

    return dic