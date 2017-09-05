def main():
    with open('../staff_wr_sample/9.mes.utf', 'r') as f:
        raw_text = f.readlines()

    preprocessed_text = preprocess(raw_text)
    print(preprocessed_text)


def preprocess(raw_text):
    preprocessed_text = ''

    if isinstance(raw_text, str):
        text_list = raw_text.splitlines()

    else:
        text_list = raw_text
    #
    # for line in text_list:
    #
    #
    #     forward, backward = cut_text(raw_text, '総括')

    return raw_text


# def cut_text(text, tag):
#
#
#     return foward, backward


if __name__ == '__main__':
    main()