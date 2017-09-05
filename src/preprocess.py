from collections import OrderedDict

# global variables
TAGS = ['総括',
        '課題・問題',
        'Highlight',
        'Other',
        'AR',
        '次週']

def main():
    with open('../staff_wr_sample/test.txt', 'rb') as f:
        # raw_text = f.readlines()
        raw_text = f.read().decode()

    preprocessed_text = preprocess(raw_text)
    # print(preprocessed_text)


def preprocess(raw_text):

    text_list = text2list(raw_text)

    content = OrderedDict()

    for tag in TAGS:
        content[tag] = search_tag(tag, text_list)

    for key, obj in content.items():
        print(key, obj)
        print('---------------')

    return content


def search_tag(tag, text_list):
    tag_flag = 0
    tag_content = []
    for text in text_list:
        if tag_flag:
            # for t in TAGS:
            #     if text.find(t) >= 0:
            #         continue
            #     else:
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

    while True:
        try:
            text_list.remove('')
        except:
            break

    return text_list


if __name__ == '__main__':
    main()