import analyze
import preprocess
import glob
import pickle
import sys


# 入力されたファイル名のWRを全て解析
def WR_analyze(WR_list, value_list):

    for WR_name in WR_list:
        with open(WR_name, 'r') as f:
            # raw_text = f.readlines()
            raw_text = f.read()
        print(raw_text)
        preprocessed_text = preprocess.preprocess(raw_text)
        analyze_dict = (analyze.analyze(preprocessed_text))
        analyze_dict['WR_name'] = WR_name
        value_list.append(analyze_dict)
        i += 1
    return value_list


def main():
    # WR_list = glob.glob('../staff_wr_sample/*.utf')  # 拡張子がutfのファイル(WR)のファイル名をリスト形式で取得
    # WR_list = glob.glob(sys.argv[1])  # 拡張子がutfのファイル(WR)のファイル名をリスト形式で取得
    WR_list = sys.argv

    WR_list.pop()
    del WR_list[0]

    print("sys arg", sys.argv)
    print("WR LIST", WR_list)

    value_list = []

    value_list = WR_analyze(WR_list, value_list)  # 全てのWRを解析

    # print(value_list)

    # with open('../staff_wr_sample/WR_analyze_result.pickle', 'wb') as pcl:
    with open(sys.argv[len(sys.argv) - 1], 'wb') as pcl:
        pickle.dump(value_list, pcl)  # リストをpickleへ保存

    with open(sys.argv[len(sys.argv) - 1], 'rb') as pcl:
        result_pickle = pickle.load(pcl)  # pickleの読込み
        print("\n----------------------------- ↓ pickle ↓ -----------------------------\n\n" + \
              str(result_pickle) + \
              "\n\n----------------------------- ↑ pickle ↑ -----------------------------")


if __name__ == '__main__':
    main()
