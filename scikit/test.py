from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re

cv = CountVectorizer(analyzer='word', ngram_range=(3,3), min_df = 2)

try:
    sample_file = 'sample_text.txt'
    sample_text = open(sample_file, 'r').read()
    sample_sentences = re.split('[.?!]', sample_text)
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

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

db = DBSCAN(eps=0.3, min_samples=3).fit(train_data_features)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
              % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
              % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
              % metrics.silhouette_score(X, labels))