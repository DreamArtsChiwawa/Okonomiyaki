import numpy as np
import matplotlib.pyplot as plt
import sys
import pickle
from google.cloud import language
import pickle
from datetime import datetime
import preprocess

SCORE_THRESHOLD = 0.8


def analyze(text):

    language_client = language.Client()

    document = language_client.document_from_html(text)

    annotations = document.annotate_text(include_sentiment=True,
                                         include_syntax=False,
                                         include_entities=False)

    value_dict = set_dict(annotations)

    return value_dict


def set_dict(annotations):

    score = annotations.sentiment.score
    magnitude = annotations.sentiment.magnitude
    score_list = []
    sentence_list = []

    for index, sentence in enumerate(annotations.sentences):
        score_list.append(sentence.sentiment.score)
        sentence_list.append(sentence.content)
   

    # print(text_list)
    sum_score = sum(score_list)

    if len(score_list) != 0:
        ave_score = sum_score / len(score_list)

    else:
        ave_score = 0

    # print(score_list)
    max_score = max(score_list)
    min_score = min(score_list)
    mid_score = np.median(score_list)
    total_score = score
    
    dic = {'max': {'score': max_score, 'sentence': sentence_list[score_list.index(max_score)]},
               'min': {'score': min_score, 'sentence': sentence_list[score_list.index(min_score)]},
               'sum': sum_score,
               'ave': ave_score,
               'mid': {'score': mid_score},
               'magnitude': magnitude,
               'total': total_score,
               'score_list': score_list
               }

    return dic


def save_fig(score_list):

    file_name = "fig_histogram.png"
    plt.figure()
    plt.hist(score_list, bins=np.arange(-1.0, 1.01, 0.1), )  # 度数分布表の取得
    plt.savefig(file_name)


def open_old_WR(info):
    path = '../pickle/' + info + '.pickle'
    with open(path, 'rb') as pcl:
        result_pickle = pickle.load(pcl)

    filename_list = result_pickle.keys()

    max_score_list = []
    max_sentence_list = []
    min_score_list = []
    min_sentence_list = []
    all_score_list = []

    for fname in filename_list:
        max_score = result_pickle[fname]['max']['score']
        if abs(max_score) >= SCORE_THRESHOLD:
            max_score_list.append(max_score)
            max_sentence_list.append(result_pickle[fname]['max']['sentence'])

        min_score = result_pickle[fname]['min']['score']
        if abs(min_score) >= -SCORE_THRESHOLD:
            min_score_list.append(min_score)
            min_sentence_list.append(result_pickle[fname]['min']['sentence'])

        all_score_list += result_pickle[fname]['score_list']

    dic = {'max_score_list': max_score_list,
           'max_sentence_list': max_sentence_list,
           'min_score_list': min_score_list,
           'min_sentence_list': min_sentence_list,
           'all_score_list': all_score_list
           }

    return dic


def main():

    print(open_old_WR('staff_wr_sample'))


if __name__ == '__main__':
    main()
