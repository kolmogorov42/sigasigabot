# -*- coding: utf-8 -*-
import re
import random


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
    return text.replace('"', '').split()


def match(text, sl):
    nsl = list(sl)
    for token in tokenize(text):
        nsl = filter(lambda x: re.search(r'\b' + token + r'\b', x['text'], flags=re.I | re.U), nsl)
    return nsl


def randomSample(sample_size, population):
    if len(population) < sample_size:
        return population
    sample = []
    for i, elem in enumerate(population):
        if i < sample_size:
            sample.append(elem)
        elif random.random() < sample_size / float(i + 1):
            replace = random.randint(0, len(sample) - 1)
            sample[replace] = elem
    return sample
