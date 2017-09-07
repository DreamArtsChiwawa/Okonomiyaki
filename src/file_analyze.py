import analyze
import preprocess
import pickle
import sys
from tqdm import tqdm


# 入力されたファイル名のWRを全て解析
def WR_analyze(WR_list):

    week_dic = {}

    for WR_name in tqdm(WR_list):
        try:
            with open(WR_name, 'r') as f:
                try:
                    raw_text = f.read()
                
                except:
                    print(WR_name, "READ ERROR")
                    continue
         
            preprocessed_text = preprocess.preprocess(raw_text)
            if(len(preprocessed_text) <= 0):
                continue
            analyze_dict = (analyze.analyze(preprocessed_text))

            week_dic[WR_name] = analyze_dict
        except:
<<<<<<< HEAD
            print(WR_name, "SOME ERROR")
            continue
=======
            print("DICTIONARY ERROR", preprocessed_text)
            exit(1)
>>>>>>> 828d126695a0ffe02e0c0d38a79b6362f82ad2bb

    return week_dic


def main():

    WR_list = sys.argv

    del WR_list[0]  # 先頭の要素(第一引数:WRが置いてある場所のパス指定)を削除

    week_dic = WR_analyze(WR_list)  # 全てのWRを解析

    # パスから'20YY年XX月'の文字列を抽出
    tmp = sys.argv[0]
    index = tmp.rfind('/')
    tmp = tmp[:index]
    index = tmp.rfind('/')
    tmp = tmp[index:]
    tmp = tmp[1:]
    filename = tmp

    with open('../pickle/' + filename + '.pickle', 'wb') as pcl:
        pickle.dump(week_dic, pcl)  # リストをpickleへ保存

if __name__ == '__main__':
    main()
