import collections


def get_top_words(words, top_size=10) -> 'collections.Counter list':
    return collections.Counter(words).most_common(top_size)