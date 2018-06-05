#!/usr/bin/env python

import sys
import os
import json
import codecs
import random
from credentials import TOKEN
from telegram.ext import Updater

random.seed(None)

sys.path.append(os.path.join(os.path.abspath('.'), 'venv/Lib/site-packages'))
MAX_RESULTS = 50

AVATAR_SIZE = 64

# construct list of SIGARETTOes
sf = codecs.open('res/sigaclean.txt', 'r', 'utf-8')
sl = json.load(sf)

# example of sl:
# sl = [
#     {'id': 1, 'text': 'SIGARETTO fa cose buffe', 'authorid': 1},
#     ...
# ]

LAST_SIGA_ID = len(sl)
# SIGARETTO id's are 1-based
