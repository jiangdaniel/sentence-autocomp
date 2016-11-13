from ml import TextProcessor as TP
from sklearn.feature_extraction.text import CountVectorizer

class Lexicon:
    def __init__(self):
        self.sentences = []

    def _add_sentence(self, sentence):
        self.sentences.append(sentence)

    def add_text(self, text):
        clusters = TP.process(text)

        for cluster in clusters:
            if len(cluster) == 1:
                newSentence = StaticSentence(cluster.pop())
            else:
                newSentence = VariableSentence.create(list(cluster))
            self.sentences.append(newSentence)

        self.print_sentences()

    def read_input(self):
        # FIXME
        pass

    def print_sentences(self):
        for sentence in self.sentences:
            print(sentence)

    def construct_trie(self):
        def add_words(trie, words):
            if len(words) == 0:
                return
            word = words.pop(0)
            if not trie.has_child(word):
                trie.add_child(word)
            add_words(trie.get_child(word), words)

        root = Trie(None)
        for sentence in self.sentences:
            words = sentence.split()
            add_words(root, words)
        return root


class Sentence:
    """ Represents a generic sentence. """

    def __init__(self, data, num_params=0):
        self.data = data
        self.numParams = num_params

    def get_num_params(self):
        return self.num_params

    def __str__(self):
        return '"' + self.data + '"'

class StaticSentence(Sentence):

    def __init__(self, data):
        super().__init__(data, 0)

class VariableSentence(Sentence):
    def create(variations):
        # FIXME
        assert len(variations) > 0
        if (len(variations) == 1):
            return StaticSentence(variations[0])

        # This requires further implementation
        result = variations[0]

        return VariableSentence(result)

    def and_array(matrix):
        """Combines a m x n matrix in a single array of length n.

        This array stores the minimum value of each column. Thus, the array
        stores the minimum number of times an ngram appears.
        """
        assert len(matrix) > 0, "Given array is too short"
        result = [10000] * len(matrix[0])
        for array in matrix:
            for j in range(len(array)):
                result[j] = min(array[j], result[j])
        return result


def naive_search(variations):
    split_variations = split(variations)
    master_sent = split_variations[0]
    for i in range(1, len(split_variations)):
        other_sent = split_variations[i]

        master_i = 0
        other_i = 0

        master_word = master_sent[master_i]
        other_word = other_sent[other_i]

        if master_word == other_word:
            master_i += 1
            other_i += 1

        else:
            # Search for the occurence
            # If you can't find it


def split(variations):
    result = []
    for sent in variations:
        result.append(sent.split())
    return result


class Trie:
    def __init__(self, val):
        self.val = val
        self.children = dict()

    def has_child(self, val):
        return val in self.children

    def get_child(self, val):
        return self.children[val]

    def add_child(self, val):
        self.children[val] = Trie(val)
