from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import numpy as np
import re

# min_df sets the number of times a ngram must repeat to be inclduded in info vector
# With 1, all ngrams are included
# With 2, only ngrams that repeat at least once are included
cv = CountVectorizer(analyzer='word', ngram_range=(2,2), min_df = 1)

try:
    sample_file = 'sample_text.txt'
    sample_text = open(sample_file, 'r').read()
    sample_sentences = re.split('[.?!]', sample_text)
    for i in range(len(sample_sentences)):
        sample_sentences[i] = sample_sentences[i].strip()
except IOError:
    sample_sentences = [u'The quick brown fox jumped over the lazy brown dog.', u'The quick thinking hare jumped over the moon.']

print("Sentences analyzed")
for text in sample_sentences:
    print(text.strip())
print()

train_data_features = cv.fit_transform(sample_sentences).toarray()
print("(number of entries, number of features):")
print(train_data_features.shape)
print()

print("Features found - repeating tokens - and frequency")
vocab = cv.get_feature_names()
dist = np.sum(train_data_features, axis=0)
for tag, count in zip(vocab, dist):
    print (count, tag)

# esp - the distance samples must be within of each other to become a core sample
# increasing this number will make the categories more inclusive

# min_samples - the minimum number of simmilar samples required to become a core sample
# Increasing this number will require there to be more occurences of a sentence structure
# to become recognized as a group

db = DBSCAN(eps=1.45, min_samples=4).fit(train_data_features)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print()

for cat, sent in zip(labels, sample_sentences):
    print(cat, sent)
