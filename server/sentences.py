class Lexicon:
    def __init__(self):
        self.sentences = []

    def _add_sentence(self, sentence):
        self.sentences.append(sentence)

    def read_input(self):
        pass

class Sentence:
    """ Represents a generic sentence. """

    def __init__(self, data, num_params=0):
        self.data = data
        self.numParams = num_params

    def get_num_params(self):
        return self.num_params

class StaticSentence(Sentence):

    def __init__(self, data):
        super().__init__(data, 0)

class VariableSentence(Sentence):
    pass

class TextProcessor:
    pass
