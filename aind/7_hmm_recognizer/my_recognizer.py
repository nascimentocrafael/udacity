import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    # return probabilities, guesses
    #raise NotImplementedError

    test_sequences = list(test_set.get_all_Xlengths().values())
    for test_X, test_Xlength in test_sequences:
        probs = {}
        best_word = None
        best_logL = float("-inf")
        for word, model in models.items():
            try:
                logL = model.score(test_X, test_Xlength)
                if logL > best_logL:
                    best_logL = logL
                    best_word = word
                probs[word] = logL
            except:
                pass
        probabilities.append(probs)
        guesses.append(best_word)
    return probabilities, guesses
