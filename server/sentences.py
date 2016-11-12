from ml import TextProcessor as TP

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
        result = ""
        return VariableSentence(result)
