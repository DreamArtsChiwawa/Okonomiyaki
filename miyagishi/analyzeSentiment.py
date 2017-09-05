"""Demonstrates how to make a simple call to the Natural Language API."""

import argparse
import numpy as np
from google.cloud import language
import sys
sys.path.append('../johejo/')
import head

def print_result(annotations):
    score = annotations.sentiment.score
    magnitude = annotations.sentiment.magnitude
    score_list = []
    
    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))
        #print(annotations.sentences)
        score_list.append(sentence_sentiment)

    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    
    sum_score = sum(score_list)
    ave_score = sum_score/len(score_list)
    max_score = max(score_list)
    min_score = min(score_list)
    center_score = np.median(score_list)

    print(score_list)
    
    print('total score is {}'.format(sum_score))
    print('average score is {}'.format(ave_score))
    print('max score is {}'.format(max_score))
    print('min score is {}'.format(min_score))
    print('center score is {}'.format(center_score))
    
    #dic = ['max':max_score, 'min':min_score, 'sum':sum_score, 'ave':ave_score]

    #return dic
    return 0

    '''
    print('Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    return 0
    '''


#def analyze(movie_review_filename):
def analyze():
    """Run a sentiment analysis request on text within a passed filename."""
    language_client = language.Client()

    review_file = head.get_text('../johejo/1061.mes.utf')
    review_file = review_file.replace('¥n','\n')
    print(review_file)
    #with open(movie_review_filename, 'r') as review_file:
    # Instantiates a plain text document.
    document = language_client.document_from_html(review_file)

    # Detects sentiment in the document.
    annotations = document.annotate_text(include_sentiment=True,
                                         include_syntax=False,
                                         include_entities=False)

    # Print the results
    print_result(annotations)

if __name__ == '__main__':
    
    '''
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'movie_review_filename',
        help='The filename of the movie review you\'d like to analyze.')
    args = parser.parse_args()
    '''
    analyze()
    #analyze(args.movie_review_filename)
