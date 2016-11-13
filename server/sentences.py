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

        self.trie = self.construct_trie()


    def read_input(self):
        # FIXME
        pass

    def print_sentences(self):
        for sentence in self.sentences:
            print(sentence)

    def complete(self, start):
        """Given the start of a sentence predict the rest of it"""
        assert self.trie != None, "No training has been done"
        words = start.split(' ')
        progress = self.trie
        for word in words:
            if not progress.has_child(word):
                return None
            progress = progress.get_child(word)
        prediction = ""

        next_trie = progress.most_likely_child()
        while next_trie != None:
            next_word = next_trie.val
            prediction += next_word + " "
            progress = progress.get_child(next_word)
            next_trie = progress.most_likely_child()

        if len(prediction) > 0:
            return prediction[:-1]
        else:
            return prediction

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
    

    def split(self):
        return self.data.split()

class StaticSentence(Sentence):

    def __init__(self, data):
        super().__init__(data, 0)

    def __repr__(self):
        return "StaticSentence('%s', 0)" % self.data

    def behead(self):
        """Returns a tuple consisting of the first word and a sentence
        with the of the sentence after the first word.
        """

        split = self.data.find(' ')
        if split == -1:
            return (self.data,)
        else:
            word = self.data[:split]
            rest = StaticSentence(self.data[split + 1:])
            return (word, rest)

class VariableSentence(Sentence):
    def create(variations):
        assert len(variations) > 0
        if (len(variations) == 1):
            return StaticSentence(variations[0])

        def naive_merge(words1, words2):
            result = []
            i1, i2 = 0, 0
            while True:
                if i1 >= len(words1) or i2 >= len(words2):
                    if i1 < len(words1) or i2 < len(words2):
                        result.append('%s')
                    break
                if (words1[i1] == words2[i2]):
                    result.append(words1[i1])
                    i1 += 1
                    i2 += 1
                else:
                    if len(result) == 0 or result[-1] != '%s':
                        result.append('%s')
                    next_i1 = next_index(words2[i2], words1, i1 + 1)
                    next_i2 = next_index(words1[i1], words2, i2 + 1)
                    if next_i2 >= 0:
                        i2 = next_i2
                    elif next_i1 >= 0:
                        i1 = next_i1
                    else:
                        i1 += 1
                        i2 += 1
            return result

        def next_index(el, lst, start):
            for i in range(start, len(lst)):
                if lst[i] == el:
                    return i
            return -1

        master = variations[0].split()
        for i in range(1, len(variations)):
            master = naive_merge(master, variations[i].split())

        return VariableSentence(' '.join(master))

class Trie:
    def __init__(self, val, chil = None):
        self.val = val
        if chil:
            self.children = chil
        else:
            self.children = dict()

    def has_child(self, val):
        return val in self.children

    def get_child(self, val):
        return self.children[val]

    def add_child(self, val):
        self.children[val] = Trie(val)

    def num_children(self):
        return len(self.children)

    def is_leaf(self):
        return self.num_children() == 0

    def most_likely_child(self):
        """Returns the likely child"""
        # Until the children obtain weights, just return a random child
        return self.random_child()

    def random_child(self):
        """Returns a random child if not leaf, else None"""
        if self.is_leaf():
            return None

        key_iter = self.children.keys().__iter__()
        return self.children[next(key_iter)]

    def __repr__(self):
        return "Trie(%s, ...)" % (self.val.__repr__())
