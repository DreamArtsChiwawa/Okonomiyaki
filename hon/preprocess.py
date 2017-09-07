from collections import OrderedDict

# global variables
TAGS = ['総括',
        '課題・問題',
        'Highlight',
        'Other',
        'AR',
        '次週']

IGNORE = ['◇',
          '◆',
          '●',
          '○',
          '○',
          '==',
          '--',
          'ーー',
          '＝＝',
          ':',
          '：',
          '*',
          '＊',
          ]

SENTENCE_TH = 5


def main():
    with open('../staff_wr_sample/1061.mes.utf', 'rt') as f:
        # raw_list = f.readlines()
        raw_text = f.read()

    print(preprocess(raw_text))


def preprocess(raw_text):

    text_list = text2list(raw_text)
    text_list = select_line(text_list)
    text_list = remake_sentence(text_list)
    text = list2text(text_list)

    return text


def list2text(input_list):

    text = ''

    for line in input_list:
        text += line + '\n'

    return text


def select_line(raw_list):

    text_list = []

    for line in raw_list:
        tmp = line.strip()
        if tmp.find('。') + tmp.find('、') >= 0 and (pre_search(tmp)):
            text_list.append(tmp)

    return text_list


def remake_sentence(input_list):

    text = ''

    for line in input_list:
        text += line

    # print(text)
    text_list = text.split('。')
    text_list = remove_blank(text_list)
    # print(text_list)

    return text_list


def pre_search(line):
    for tag in TAGS:
        if line.find(tag) >= 0:
            return False

    for tag in IGNORE:
        if line.find(tag) >= 0:
            return False

    return True


def old_preprocess(raw_text):

    text_list = text2list(raw_text)

    content = OrderedDict()

    for tag in TAGS:
        content[tag] = search_tag(tag, text_list)

    sentences = []
    for key, value in content.items():
        sentence = ''
        for v in value:
            sentence += v

        tmp = sentence.split('。')
        tmp = remove_blank(tmp)
        for item in tmp:
            sentences.append(item)

    result = ''
    for s in sentences:
        result += s + "\n"

    return result


def search_tag(tag, text_list):
    tag_flag = 0
    tag_content = []
    for text in text_list:
        if tag_flag:
            for t in TAGS:
                if tag_flag == 0:
                    break
                if text.find(t) >= 0 or (tag == t == '次週' and text.find("。") < 0 and text.find("、") < 0):
                    tag_flag = 0
                    continue
            if tag_flag == 0:
                break
            tag_content.append(text)

        if text.find(tag) >= 0:
            tag_flag = 1
            continue

    return tag_content


def text2list(raw_text):
    if isinstance(raw_text, str):
        text_list = raw_text.splitlines()

    else:
        text_list = raw_text

    for i in range(len(text_list)):
        text_list[i] = text_list[i].strip()

    text_list = remove_blank(text_list)

    return text_list


def remove_blank(list_obj):
    while True:
        try:
            list_obj.remove('')
        except:
            break

    return list_obj


if __name__ == '__main__':
    main()
