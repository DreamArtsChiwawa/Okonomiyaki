def main():
    with open('../staff_wr_sample/9.mes.utf', 'r') as f:
        # raw_text = f.readlines()
        raw_text = f.read()

    preprocessed_text = preprocess(raw_text)


def preprocess(raw_text):
    preprocessed_text = ''

    if isinstance(raw_text, str):
        print('IF')
        text_list = raw_text.splitlines()

    else:
        print('ELSE')
        text_list = raw_text

    print(text_list)

    return text_list


# def cut_text(text, tag):
#
#
#     return foward, backward


if __name__ == '__main__':
    main()