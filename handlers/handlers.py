import random
import utils
import telegram
import uuid

from message_handler import logger
from bot import sl, MAX_RESULTS, LAST_SIGA_ID, AVATAR_SIZE
from media import videos
import gen
import notfound


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def getS(sl, n_siga):
    return sl[n_siga - 1]


def normalSearch(q, sl):
    return utils.randomSample(MAX_RESULTS, utils.match(q, sl))


def parseSigaNumber(q):
    if q.startswith('#'):
        try:
            n_siga = int(q[1:])
            if 1 <= n_siga <= LAST_SIGA_ID:
                return n_siga
            return False
        except ValueError:
            return False
    return False


def parseInlineQuery(bot, update):
    q = update.inline_query.query

    # actual inline query results to present to the user
    results = []

    if q.lower() == 'gen':
        # if it's simply 'gen', we fill our results with a generated SIGARETTO
        restext = gen.generate()
        results.append(telegram.InlineQueryResultArticle(
            type='article',
            id=uuid.uuid4(),
            thumb_url=utils.thumbnail(),
            thumb_width=AVATAR_SIZE,
            thumb_height=AVATAR_SIZE,
            title='SIGARETTO #GENERATED',
            description=restext[:200],
            input_message_content=telegram.InputTextMessageContent(message_text=restext, parse_mode=None)
        ))

    else:
        # we have to search
        # search results:
        res = []

        # try to detect if user asked for a SIGA id
        asked_siga = parseSigaNumber(q)
        if asked_siga:
            # yes, pick it
            res = [getS(sl, asked_siga)]
        else:
            # no, regular query matching
            res = normalSearch(q, sl)

        # search completed, we now have all matching results in res, which may or may not be empty
        if not res:
            # empty, send bogus SIGA
            restext = random.choice(notfound.notfound)
            if "%s" in restext:
                restext = restext % q
            results.append(telegram.InlineQueryResultArticle(
                type='article',
                id=uuid.uuid4(),
                thumb_url=utils.thumbnail(),
                thumb_width=AVATAR_SIZE,
                thumb_height=AVATAR_SIZE,
                title='SIGARETTO #NOT_FOUND',
                description=restext[:200],
                input_message_content=telegram.InputTextMessageContent(message_text=restext, parse_mode=None)
            ))

        else:
            # non-empty, build list of actual results
            for i in res:
                restext = i['text']
                sid = i['id']
                authorid = i['authorid']

                # if sid in img_cache:
                #     results.append(telegram.InlineQueryResultPhoto(
                #         type='photo',
                #         id=sid,
                #         photo_url=img_url(sid),
                #         thumb_url=utils.thumbnail(authorid),
                #         title='SIGARETTO #%d' % sid,
                #         description=restext[:200],
                #         caption=restext[:200],
                #         photo_file_id=img_cache[sid],
                #     ))
                # elif sid in audio_cache:
                #     results.append(telegram.InlineQueryResultAudio(
                #         type='audio',
                #         id=sid,
                #         audio_url=audio_url(sid),
                #         title='SIGARETTO #%d' % sid,
                #         caption=restext[:200]
                #         # to be completed with other parameters
                #     ))

                fulltext = restext
                if sid in videos:
                    fulltext = restext + "\n\n" + videos[sid]
                results.append(telegram.InlineQueryResultArticle(
                    type='article',
                    id=sid,
                    thumb_url=utils.thumbnail(authorid),
                    thumb_width=AVATAR_SIZE,
                    thumb_height=AVATAR_SIZE,
                    title='SIGARETTO #%d' % sid,
                    description=restext[:200],
                    input_message_content=telegram.InputTextMessageContent(message_text=fulltext, parse_mode=None)
                ))

    # all cases examined, we now have a results array and can answer the query
    bot.answerInlineQuery(update.inline_query.id, results, cache_time=0)

    logger.info(update)
