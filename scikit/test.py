from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

cv = CountVectorizer(analyzer='word', ngram_range=(3,3), min_df = 2)

try:
    sample_text = open('sample_text.txt', 'r')
    corpus = sample_text.read().split('.')
except IOError:
    corpus = [u'The quick brown fox jumped over the lazy brown dog.', u'The quick thinking hare jumped over the moon.']

print("Sentences analyzed")
for text in corpus:
    print(text)
print()

train_data_features = cv.fit_transform(corpus).toarray()
print("(number of entries, number of features):")
print(train_data_features.shape)
print()

print("Features found - repeating tokens - and frequency")
vocab = cv.get_feature_names()
dist = np.sum(train_data_features, axis=0)
for tag, count in zip(vocab, dist):
    print (count, tag)

