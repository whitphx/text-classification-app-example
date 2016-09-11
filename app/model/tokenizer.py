# -*- coding: utf-8 -*-
import MeCab
import neologdn
import re


class MeCabTokenizer(object):
    def __init__(self, dicpath=None):
        self.dicarg = '' if dicpath is None else ' -d ' + dicpath

        self.tagger = MeCab.Tagger('-Ochasen' + self.dicarg)
        self.rx_url = re.compile('https?://[\w/:%#\$&\?\(\)~\.=\+\-]+')

    def __call__(self, text):
        return self.tokenize(text)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['tagger']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.tagger = MeCab.Tagger('-Ochasen' + self.dicarg)

    def normalize_word(self, text):
        text = self.rx_url.sub('URLTOKEN', text)
        return text

    def tokenize(self, text):
        input_type = type(text)
        bow = []

        if input_type == str:
            text = text.decode('utf8')

        text = neologdn.normalize(text).encode('utf8')
        text = self.normalize_word(text)

        node = self.tagger.parseToNode(text)
        while node:
            feature = node.feature.split(',')

            if feature[0] == 'BOS/EOS':
                node = node.next
                continue

            if feature[0] in ['名詞', '動詞', '形容詞', '副詞', '連体詞']:
                word = feature[6] if feature[6] != '*' else node.surface

                if feature[1] == '数':
                    word = 'NUMTOKEN'

                if feature[1] == '接尾':
                    node = node.next
                    continue

                if input_type == unicode:
                    word = word.decode('utf8')

                bow.append(word)

            node = node.next

        return bow
