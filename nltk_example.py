import sys

from pathlib import Path
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk import pos_tag


stopword_file = Path(__file__).parent / 'english_stopwords.txt'
NOUNS = {'NN', 'NNP', 'NNPS', 'NNS'}
VERBS = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}


def get_stopwords():
    with open(stopword_file, 'r') as f:
        stopwords = f.read().splitlines()

    return set(stopwords)


def tokenize_phrase(phrase):
    return word_tokenize(phrase)


def remove_stopwords(tokens, stopwords):
    return [word for word in tokens if word not in stopwords]


def stem_words(tokens):
    p = PorterStemmer()

    return [p.stem(word) for word in tokens]

def tag_pos(tokens):
    return pos_tag(tokens)


def main():
    print('Enter a phrase to see it tokenized, stemmed, and stop words removed. Type exit to end.')

    stopwords = get_stopwords()

    while True:
        phrase = input('\nEnter phrase: ')
        if phrase == 'exit':
            break

        result = stem_words(remove_stopwords(tokenize_phrase(phrase), stopwords))
        result_pos = tag_pos(result)

        print('Results: {0}'.format(result))
        print('Nouns: {0}'.format([w for w, p in result_pos if p in NOUNS]))
        print('Verbs: {0}'.format([w for w, p in result_pos if p in VERBS]))


if __name__ == "__main__":
    main()
