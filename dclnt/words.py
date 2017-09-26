import nltk
from nltk import pos_tag


try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')


def get_words_from_names(names):
    words = []
    for func_name in names:
        words += func_name.split('_')
    # TODO: sometimes split get empty strings
    words = list(filter(bool, words))
    print('{} words extracted.'.format(len(words)))
    return words


def pass_all_words(words):
    return words


def get_pof_from_words(words, pof_tag) -> list:
    # TODO: strange behavior of NLTK: verb tag on non-verb words
    if pof_tag == 'ALL':
        return words
    parts_of_speech = [item[0] for item in pos_tag(words) if item[1][:2] == pof_tag]
    print('{} parts of speech filtered'.format(len(parts_of_speech)))
    return parts_of_speech
