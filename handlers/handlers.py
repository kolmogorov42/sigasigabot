import random
import utils
import telegram
import uuid

from message_handler import logger
from bot import sl, MAX_RESULTS, LAST_SIGA_ID
from media import images, sounds, videos, img_cache, audio_cache
import gen
import notfound


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def getS(sl, n_siga):
    return sl[n_siga + 1]


def pickSiga(bot, update, n_siga=None):
    # n_siga: 1-based SIGARETTO index
    if not n_siga:
        randomSiga(bot, update)
        return

    if n_siga in images:
        try:
            file_id = img_cache[n_siga]
            bot.sendPhoto(
                chat_id=update.message.chat_id,
                photo=file_id,
                caption=getS(sl, n_siga)['text'].encode('utf8'))
        except KeyError:
            msg = bot.sendPhoto(
                chat_id=update.message.chat_id,
                photo=open('res/media/%d.jpg' % n_siga, 'rb'),
                caption=getS(sl, n_siga)['text'].encode('utf8'))

    elif n_siga in sounds:
        try:
            file_id = audio_cache[n_siga]
            bot.sendAudio(
                chat_id=update.message.chat_id,
                audio=file_id,
                title=sounds[n_siga].encode('utf8'),
                performer="Cani in Alto",
                caption=getS(sl, n_siga)['text'].encode('utf8'))
        except KeyError:
            msg = bot.sendAudio(
                chat_id=update.message.chat_id,
                audio=open('res/media/%d.mp3' % n_siga, 'rb'),
                title=sounds[n_siga].encode('utf8'),
                performer="Cani in Alto",
                caption=getS(sl, n_siga)['text'].encode('utf8'))

    elif n_siga in videos:
        bot.sendMessage(
            update.message.chat_id,
            text=getS(sl, n_siga)['text'] + '\r\n' + videos[n_siga])

    else:
        try:
            siga = getS(sl, n_siga)['text']
            bot.sendMessage(update.message.chat_id, text=siga)
        except KeyError:
            randomSiga(bot, update)


def randomSiga(bot, update):
    n_siga = random.randint(1, LAST_SIGA_ID)
    pickSiga(bot, update, n_siga)


def parseMsgNumber(bot, update):
    try:
        n_siga = int(update.message.text)
    except ValueError:
        n_siga = None
    pickSiga(bot, update, n_siga)


def parseInlineQuery(bot, update):
    q = update.inline_query.query

    if q == 'gen':
        results = []
        restext = gen.generate()
        results.append(telegram.InlineQueryResultArticle(
            type='article',
            id=uuid.uuid4(),
            thumb_url='http://i.imgur.com/Msphffb.jpg',
            thumb_width=64,
            thumb_height=64,
            title='SIGARETTO',
            description=restext[:200],
            input_message_content=telegram.InputTextMessageContent(message_text=restext, parse_mode=None)
        ))

        bot.answerInlineQuery(update.inline_query.id, results, cache_time=0)

    else:
        res = utils.match(q, sl)
        res = utils.randomSample(MAX_RESULTS, res)

        results = []
        for i in res:
            restext = i['text']
            results.append(telegram.InlineQueryResultArticle(
                type='article',
                id=uuid.uuid4(),
                thumb_url='http://i.imgur.com/Msphffb.jpg',
                thumb_width=64,
                thumb_height=64,
                title='SIGARETTO',
                description=restext[:200],
                input_message_content=telegram.InputTextMessageContent(message_text=restext, parse_mode=None)
            ))

        bot.answerInlineQuery(update.inline_query.id, results, cache_time=0)

    logger.info(update)
