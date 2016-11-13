from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN
import numpy as np
import re

class TextProcessor:

    """ Parameters used by _init_CountVectorizer to initialize CountVectorizer """
    CV_PARAMS = {
        'analyzer': 'word',
        'ngram_range': (2, 2),
        'min_df': 1
    }

    """ Parameters used by _init_DBSCAN to initialize DBSCAN """
    DB_PARAMS = {
        'eps': 1.45,
        'min_samples': 4
    }

    """ Regex pattern used to split text into sentences """
    DELIMITER_REGEX = '[.?!]'

    def __init__(self):
        pass

    """ Takes in a block of text and returns a list of sentence sets that contain close variations of a sentence """
    def process(text):
        vectorizer = TextProcessor._init_CountVectorizer();
        sentences = TextProcessor._format_text(text)
        train_data = vectorizer.fit_transform(sentences).toarray()

        # vocab = vectorizer.get_feature_names()
        # dist = np.sum(train_data, axis=0)
        # for tag, count in zip(vocab, dist):
        #     print (count, tag)

        # CLUSTERING
        clusterer = TextProcessor._init_DBSCAN()
        clusterer.fit(train_data)
        # core_samples_mask = np.zeros_like(clusterer.labels_, dtype=bool)
        # core_samples_mask[clusterer.core_sample_indices_] = True


        # Labels designate the clusters found
        # -1 is the grab bag or outlier cluster
        labels = clusterer.labels_

        num_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        clusters = []

        for _ in range(num_clusters):
            clusters.append(set())

        for label, sentence in zip(labels, sentences):
            if label == -1:
                continue
            clusters[label].add(sentence)

        return clusters

    def _format_text(text):
        def _split_text(text):
            return re.split(TextProcessor.DELIMITER_REGEX, text)

        def _strip_text(text):
            return text.strip()
        split_text = _split_text(text)
        split_text = list(map(_strip_text, split_text))
        return split_text



    def _init_DBSCAN():
        return DBSCAN(**TextProcessor.DB_PARAMS)

    def _init_CountVectorizer():
        return CountVectorizer(**TextProcessor.CV_PARAMS)
