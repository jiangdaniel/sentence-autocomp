from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(analyzer='word', ngram_range=(3,3), min_df = 2)

try:
    sample_text = open('sample_text.txt', 'r')
    corpus = sample_text.read().split('.')
except IOError:
    corpus = [u'The quick brown fox jumped over the lazy brown dog.', u'The quick thinking hare jumped over the moon.']

for text in corpus:
    print(text)
print()

print(cv.fit_transform(corpus).toarray())

for pair in cv.get_feature_names():
    print(pair)

