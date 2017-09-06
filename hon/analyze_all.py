import analyze
import preprocess

def main():
    with open('../staff_wr_sample/1124.mes.utf', 'rb') as f:
        # raw_text = f.readlines()
        raw_text = f.read().decode()

    preprocessed_text = preprocess.preprocess(raw_text)
    value = analyze.analyze(preprocessed_text)


if __name__ == '__main__':
    main()
