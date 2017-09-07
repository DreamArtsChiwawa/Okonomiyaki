import analyze
import preprocess
import glob
import pickle
import sys
from tqdm import tqdm

# 入力されたファイル名のWRを全て解析
def WR_analyze(WR_list, value_list):
    week_dic = {}

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
        value_list.append(analyze_dict)

        week_dic[WR_name] = analyze_dict

    #print(week_dic)
    return week_dic


def main():
    # WR_list = glob.glob('../staff_wr_sample/*.utf')  # 拡張子がutfのファイル(WR)のファイル名をリスト形式で取得
    # WR_list = glob.glob(sys.argv[1])  # 拡張子がutfのファイル(WR)のファイル名をリスト形式で取得
    WR_list = sys.argv

    #WR_list.pop()
    del WR_list[0]      # 先頭の要素(第一引数:WRが置いてある場所のパス指定)を削除

    #print("sys arg", sys.argv)
    #print("WR LIST", WR_list)

    week_dic = []

    week_dic = WR_analyze(WR_list, week_dic)  # 全てのWRを解析

    
    # パスから'20YY年XX月'の文字列を抽出
    tmp = sys.argv[0]
    index = tmp.rfind('/')
    tmp = tmp[:index]
    index = tmp.find('/')
    tmp = tmp[index:]
    tmp = tmp[1:]           
    #print(tmp)     # '20YY年XX月'が抽出できているかの確認用

    filename = tmp
    # # with open('../staff_wr_sample/WR_analyze_result.pickle', 'wb') as pcl:
    with open('../pickle/' + filename + '.pickle', 'wb') as pcl:
        pickle.dump(week_dic, pcl)  # リストをpickleへ保存

    # with open(filename, 'rb') as pcl:
    #     result_pickle = pickle.load(pcl)  # pickleの読込み
    #     print("\n----------------------------- ↓ pickle ↓ -----------------------------\n\n" + \
    #           str(result_pickle) + \
    #           "\n\n----------------------------- ↑ pickle ↑ -----------------------------")


if __name__ == '__main__':
    main()
