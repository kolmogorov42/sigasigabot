#!/usr/bin/env python

import sys
import os
import json
import codecs
import random

random.seed(None)

from cache import Cache

media_cache = Cache()

sys.path.append(os.path.join(os.path.abspath('.'), 'venv/Lib/site-packages'))

from credentials import TOKEN
from webapp2 import WSGIApplication, Route

sf = codecs.open('res/sigaclean.txt', 'r', 'utf-8')
sl = json.load(sf)

routes = [
    # Route for handle webhook (change it using admin rights, maybe..
    Route('/set_webhook', handler='handlers.hook_handler.WebHookHandler:set_webhook'),

    # Route for Telegram updates
    Route('/' + TOKEN, handler='handlers.hook_handler.WebHookHandler:webhook_handler')

]
app = WSGIApplication(routes, debug=False)
