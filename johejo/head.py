
def main():
    # print("GROUP")
    # print(get_group("/Users/heijo/PycharmProjects/Okonomiyaki/johejo/1061.mes.utf"))
    #
    # print()
    #
    # print("TEXT")
    print(get_text("1061.mes.utf"))


def get_group(path):
    group = ''
    with open(path, 'r') as f:
        text = f.readlines()

    for line in text:
        if line.find("Subject") >= 0:
            tmp = line
            tmp = tmp[:tmp.rfind("_")]
            group = tmp[tmp.rfind("_") + 1:]

    return group


def cut_text(text, tags):
    content = text[text.find(tags["tag"]) + len(tags["tag"]):]
    content = content[:content.find(tags["next_tag"])]
    # content = []
    # tag_flag = 0
    # for line in text:
    #     index = line.find(tags["tag"])
    #     if index >= 0:
    #         tag_flag = 1
    #         continue
    #     if tag_flag == 1:
    #         content.append(line.strip())
    #         continue
    #     index = line.find(tags["next_tag"])
    #     if index >= 0 and tag_flag == 1:
    #         tag_flag = 0
    #
    # result = ''
    # for line in content:
    #     result += line
    #
    # tmp = result.split("。")
    #
    # sentences = ''
    # for line in tmp:
    #     sentences += line + '\n'

    return content


def get_text(text):
    # with open(path, 'r') as f:
    #     text = f.readlines()
    #     text = f.read()
    sokatsu_tags = {"tag": "総括", "next_tag": "■課題・問題・トラブル⇒Request"}
    sokatsu_content = cut_text(text, sokatsu_tags)

    kadai_tags = {"tag": "課題・問題・トラブル⇒Request", "next_tag": "Highlight"}
    kadai_content = cut_text(text, kadai_tags)

    jisyu_tags = {"tag": "次週の指針、メッセージ", "next_tag": "\n\n"}
    jisyu_content = cut_text(text, jisyu_tags)

    all_text = sokatsu_content + kadai_content + jisyu_content

    return all_text


if __name__ == '__main__':
    main()