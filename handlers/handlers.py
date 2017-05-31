import random
import utils

from message_handler import logger
from bot import sl, media_cache
from media import images, sounds, videos
import gen
import notfound


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def pickSiga(bot, update, n_siga=0):
    if not n_siga:
        randomSiga(bot, update)
        return

    if n_siga in images:
        try:
            file_id = media_cache.get(n_siga)
            bot.sendPhoto(
                chat_id=update.message.chat_id,
                photo=file_id,
                caption=sl[n_siga]['text'].encode('utf8'))
        except KeyError:
            msg = bot.sendPhoto(
                chat_id=update.message.chat_id,
                photo=open('res/media/%d.jpg' % n_siga, 'rb'),
                caption=sl[n_siga]['text'].encode('utf8'))
            media_cache.add(n_siga, msg.photo[0].file_id)

    elif n_siga in sounds:
        try:
            file_id = media_cache.get(n_siga)
            bot.sendAudio(
                chat_id=update.message.chat_id,
                audio=file_id,
                title=sounds[n_siga].encode('utf8'),
                performer="Cani in Alto",
                caption=sl[n_siga]['text'].encode('utf8'))
        except KeyError:
            msg = bot.sendAudio(
                chat_id=update.message.chat_id,
                audio=open('res/media/%d.mp3' % n_siga, 'rb'),
                title=sounds[n_siga].encode('utf8'),
                performer="Cani in Alto",
                caption=sl[n_siga]['text'].encode('utf8'))
            media_cache.add(n_siga, str(msg.audio.file_id))

    elif n_siga in videos:
        bot.sendMessage(
            update.message.chat_id,
            text=sl[n_siga]['text'] + '\r\n' + videos[n_siga])

    else:
        try:
            siga = sl[n_siga]['text']
            bot.sendMessage(update.message.chat_id, text=siga)
        except KeyError:
            randomSiga(bot, update)


def randomSiga(bot, update):
    n_siga = random.randint(1, len(sl))
    pickSiga(bot, update, n_siga)


def parseMsgNumber(bot, update):
    try:
        n_siga = int(update.message.text)
    except ValueError:
        n_siga = None
    pickSiga(bot, update, n_siga)


def parseInlineQuery(bot, update):
    logger.info(update)


# todo write the whole function


def genSiga(bot, update):
    bot.sendMessage(update.message.chat_id, text=gen.generate())


def parseGeneral(bot, update):
    text = update.message.text
    try:
        n_siga = int(text)
        pickSiga(bot, update, n_siga)
    except ValueError:
        if text == 'gen':
            genSiga(bot, update)
        elif text == 'random':
            randomSiga(bot, update)
        else:
            results = utils.match(text, sl)
            if results:
                bot.sendMessage(update.message.chat_id, text=random.choice(results)['text'])
            else:
                chosen = random.choice(notfound.notfound)
                if "%s" in chosen:
                    bot.sendMessage(update.message.chat_id, text=(chosen % text))
                else:
                    bot.sendMessage(update.message.chat_id, text=chosen)
