from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(analyzer='word', ngram_range=(2,2), min_df = 0)

corpus = [u'The quick brown fox jumped over the lazy brown dog.', u'The quick thinking hare jumped over the moon.']
for text in corpus:
    print(text)
print()

print(cv.fit_transform(corpus).toarray())

for pair in cv.get_feature_names():
    print(pair)

