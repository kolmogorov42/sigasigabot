# -*- coding: utf-8 -*-
import re


def validateQuotes(text):
    return text.count('"') % 2 == 0


def tokenize(text):
    if validateQuotes(text):
        groups = text.split('"')
        quoted = []
        non_quoted = []
        parity = 0
        for g in groups:
            if parity:
                quoted.append(g)
            else:
                non_quoted.append(g)
            parity = 1 - parity
        # end for
        quoted = [x for x in quoted if x != '']
        non_quoted = ' '.join(non_quoted).split()

        quoted.extend(non_quoted)
        return quoted

    else:
        return text.replace('"', '').split()


def match(text, sl):
    nsl = list(sl)
    for token in tokenize(text):
        nsl = filter(lambda x: re.search(r'\b' + token + r'\b', x[1]['text'], flags=re.I), nsl)
    return nsl
