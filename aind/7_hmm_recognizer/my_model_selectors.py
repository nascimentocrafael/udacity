import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores

        best_BIC = float("inf")
        best_model = None
        for n_states in range(self.min_n_components, self.max_n_components+1):
            BIC = float("inf")
            try:
                model = self.base_model(n_states)
                logL = model.score(self.X, self.lengths)
                n = sum(self.lengths)
                p = (n_states ** 2) + 2 * n_states * n + 1
                BIC = -2 * logL + p * np.log(n)
                if BIC < best_BIC:
                    best_BIC = BIC
                    best_model = model
            except:
                break
        return best_model

class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores

        best_DIC = float("-inf")
        best_model = None

        other_words = [w for w in self.words if w != self.this_word]
        m = len(self.words)
        #print(other_words)
        for n_states in range(self.min_n_components, self.max_n_components+1):
            DIC = float("-inf")
            try:
                model = self.base_model(n_states)
                logL = model.score(self.X, self.lengths)

                #other_logL = [model.score(self.hwords[w]) for w in other_words]
                other_logL = []
                for w in other_words:
                    x, l = self.hwords[w]
                    other_logL.append(model.score(x, l))

                DIC = logL - (sum(other_logL) - logL) / (m - 1)
                if DIC > best_DIC:
                    best_DIC = DIC
                    best_model = model
            except:
                break
        return best_model

class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    ''' 

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV
        
        word_sequences = self.sequences
        split_method = KFold(2)

        k_folds = []
        for cv_train_idx, cv_test_idx in split_method.split(word_sequences):
            X_train, lenghts_train = combine_sequences(cv_train_idx, word_sequences)
            X_test, lenghts_test = combine_sequences(cv_test_idx, word_sequences)
            train = (X_train, lenghts_train)
            test = (X_test, lenghts_test)
            k_folds.append((train, test))

        best_logL = float("-inf")
        best_n = -1

        for n_states in range(self.min_n_components, self.max_n_components+1):
            avg_logL = 0.0
            try:
                model = GaussianHMM(n_components=n_states, covariance_type="diag", n_iter=1000,
                                        random_state=self.random_state, verbose=False)
                for k_train, k_test in k_folds:
                    model.fit(k_train[0], k_train[1])
                    logL = model.score(k_test[0], k_test[1])
                    avg_logL += logL
                avg_logL /= 2.0
                if avg_logL > best_logL:
                    best_logL = avg_logL
                    best_n = n_states
            except:
                break
        return self.base_model(best_n)