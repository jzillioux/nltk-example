import sys
import time

from pathlib import Path
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk import pos_tag
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


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


def entity_recognition(client, phrase):
    document = types.Document(content=phrase, type=enums.Document.Type.PLAIN_TEXT)
    entities = client.analyze_entities(document).entities

    for entity in entities:
        entity_type = enums.Entity.Type(entity.type)
        result = '=' * 20
        result += '\n' + u'{:<16}: {}'.format('name', entity.name)
        result += '\n' + u'{:<16}: {}'.format('type', entity_type.name)
        result += '\n' + u'{:<16}: {}'.format('salience', entity.salience)
        result += '\n' + u'{:<16}: {}'.format('wikipedia_url', entity.metadata.get('wikipedia_url', '-'))
        result += '\n' + u'{:<16}: {}'.format('mid', entity.metadata.get('mid', '-'))

    return result


def main():
    print('Enter a phrase to see it tokenized, stemmed, and stop words removed. Type exit to end.')

    stopwords = get_stopwords()
    client = language.LanguageServiceClient()

    while True:
        phrase = input('\nEnter phrase: ')
        if phrase == 'exit':
            break

        start = time.perf_counter()
        entity_info = entity_recognition(client, phrase)
        duration = int((time.perf_counter() - start) * 1000)

        result = tokenize_phrase(phrase)
        result_pos = tag_pos(result)
        result = stem_words(remove_stopwords(result, stopwords))

        print('Stemmed Tokens: {0}'.format(result))
        print('Nouns: {0}'.format([w for w, p in result_pos if p in NOUNS]))
        print('Verbs: {0}'.format([w for w, p in result_pos if p in VERBS]))
        print('\nGoogle Entity Info: (duration ms: {0})'.format(duration))
        print(entity_info)


if __name__ == "__main__":
    main()
