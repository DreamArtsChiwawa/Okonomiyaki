import analyze
import preprocess
import glob
import pickle
import sys
from tqdm import tqdm

# 入力されたファイル名のWRを全て解析
def WR_analyze(WR_list, value_list):

    for WR_name in tqdm(WR_list):
        with open(WR_name, 'r') as f:
            # raw_text = f.readlines()
            try:
                raw_text = f.read()
            except:
                #print(WR_name)
                continue
        #print(raw_text)
        preprocessed_text = preprocess.preprocess(raw_text)
        analyze_dict = (analyze.analyze(preprocessed_text))
        analyze_dict['WR_name'] = WR_name
        value_list.append(analyze_dict)
    return value_list


def main():
    # WR_list = glob.glob('../staff_wr_sample/*.utf')  # 拡張子がutfのファイル(WR)のファイル名をリスト形式で取得
    # WR_list = glob.glob(sys.argv[1])  # 拡張子がutfのファイル(WR)のファイル名をリスト形式で取得
    WR_list = sys.argv

    #WR_list.pop()
    del WR_list[0]      # 先頭の要素(第一引数:WRが置いてある場所のパス指定)を削除

    # print("sys arg", sys.argv)
    # print("WR LIST", WR_list)

    value_list = []

    value_list = WR_analyze(WR_list, value_list)  # 全てのWRを解析

    # print(value_list)

    # with open('../staff_wr_sample/WR_analyze_result.pickle', 'wb') as pcl:
    with open('hoge.pickle', 'wb') as pcl:
        pickle.dump(value_list, pcl)  # リストをpickleへ保存

    # with open('hoge.pickle', 'rb') as pcl:
    #     result_pickle = pickle.load(pcl)  # pickleの読込み
    #     print("\n----------------------------- ↓ pickle ↓ -----------------------------\n\n" + \
    #           str(result_pickle) + \
    #           "\n\n----------------------------- ↑ pickle ↑ -----------------------------")


if __name__ == '__main__':
    main()
