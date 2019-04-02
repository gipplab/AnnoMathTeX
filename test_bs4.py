from string import punctuation


def t(word):
    contains = not list(filter(lambda c: c in punctuation, word)) #else False
    print(contains)


t('tes/t')