
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
    return content


def get_text(path):
    with open(path, 'r') as f:
        text = f.read()

    sokatsu_tags = {"tag": "総括", "next_tag": "■課題・問題・トラブル⇒Request"}
    sokatsu_content = cut_text(text, sokatsu_tags)

    kadai_tags = {"tag": "課題・問題・トラブル⇒Request", "next_tag": "Highlight"}
    kadai_content = cut_text(text, kadai_tags)

    jisyu_tags = {"tag": "次週の指針、メッセージ", "next_tag": "¥n"}
    jisyu_content = cut_text(text, jisyu_tags)

    all_text = sokatsu_content + kadai_content + jisyu_content
    all_text.replace("-", "")
    all_text.replace("=", "")
    all_text.strip()

    return all_text


if __name__ == '__main__':
    main()