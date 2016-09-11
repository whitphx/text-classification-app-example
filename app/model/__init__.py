from os import makedirs
from os.path import dirname, join, normpath, exists
import cPickle as pickle
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from .tokenizer import MeCabTokenizer

tokenizer = MeCabTokenizer('/usr/local/lib/mecab/dic/mecab-ipadic-neologd')


class ValidationFailException(Exception):
    pass

class Model(object):
    save_dir = join(dirname(__file__), 'data')
    save_path = join(save_dir, 'model.pkl')

    def __init__(self):
        vectorizer = TfidfVectorizer(analyzer=tokenizer)
        classfier = RandomForestClassifier(n_estimators=120)
        pipeline = Pipeline([
            ('vectorizer', vectorizer),
            ('classifier', classfier),
        ])

        self.pipeline = pipeline

        self.label_names = None

    def fit(self, X, y):
        self.pipeline.fit(X, y)

    def set_label_names(self, label_names):
        self.label_names = pd.Series(label_names)

    def validate(self, text):
        if len(text) < 10:
            raise ValidationFailException('Input too short')

        return True

    def get_result(self, text):
        if self.label_names is None:
            raise Exception('label_names is not set.')

        try:
            self.validate(text)
        except ValidationFailException as e:
            return {
                'ok': False,
                'error': e.message
            }

        try:
            proba = self.pipeline.predict_proba([text])[0]
        except ValueError:
            return {
                'ok': False,
                'error': 'Invalid input',
            }

        indices = np.argsort(proba)[::-1]
        label_names_sorted = self.label_names[indices]
        proba_sorted = proba[indices]

        res = [
            {'label': l, 'proba': p}
            for l, p
            in zip(label_names_sorted, proba_sorted)
        ]

        return {
            'ok': True,
            'result': res,
        }

    def save(self):
        if not exists(self.save_dir):
            makedirs(self.save_dir)

        with open(self.save_path, 'wb') as f:
            pickle.dump(self, f, -1)

    @classmethod
    def restore(cls):
        with open(cls.save_path, 'rb') as f:
            return pickle.load(f)
