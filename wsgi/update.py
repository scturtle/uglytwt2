import bottle
from utils import *
from oauth import *
from libs import *

@bottle.route('/getinfo')
def getinfo():
    if not get_session(): bottle.abort('401')
    if not get_auth(): bottle.abort('401')
    try:
        tweet = api('get_status', id=bottle.request.GET['id'])
        if hasattr(tweet,'entities') and 'user_mentions' in tweet.entities:
            others = [u['screen_name'] for u in tweet.entities['user_mentions']]
            others = ''.join(['@'+u+' ' for u in others])
        else:
            others = ''
    except Exception,e:
        bottle.abort(500,e.message)
    return {'text':tweet.text,
            'name':tweet.author.screen_name,
            'others':others,
            'protected':tweet.author.protected}

@bottle.route('/ort')
def ort():
    if not get_session(): bottle.abort('401')
    if not get_auth(): bottle.abort('401')
    try:
        tweet = api('retweet', id=bottle.request.GET['id'])
    except tweepy.TweepError,e:
        bottle.response.status=206
        msg = e.reason.encode('utf-8').split('\n')[0]
        return msg
    return 'OK'

@bottle.route('/fav')
def fav():
    if not get_session(): bottle.abort('401')
    if not get_auth(): bottle.abort('401')
    tid = bottle.request.GET['id']
    try:
        tweet = api('get_status', id=tid)
        if tweet.favorited:
            tweet = api('destroy_favorite', id=tid)
            return 'FAV'
        else:
            tweet = api('create_favorite', id=tid)
            return 'UNFAV'
    except tweepy.TweepError,e:
        bottle.response.status=206
        msg = e.reason.encode('utf-8').split('\n')[0]
        return msg

@bottle.route('/del')
def delete():
    if not get_session(): bottle.abort('401')
    if not get_auth(): bottle.abort('401')
    try:
        tweet = api('destroy_status', id=bottle.request.GET['id'])
    except tweepy.TweepError,e:
        bottle.response.status=206
        msg = e.reason.encode('utf-8').split('\n')[0]
        return msg
    return 'OK'

@bottle.post('/update')
def update():
    if not get_session(): bottle.abort('401')
    if not get_auth(): bottle.abort('401')
    tp=bottle.request.POST['type'];
    try:
        if not tp or tp=='re' or tp=='rt':
            api('update_status',status=bottle.request.POST['twt'],
                    in_reply_to_status_id=bottle.request.POST['id'])
    except tweepy.TweepError,e:
        bottle.response.status=206
        msg = e.reason.encode('utf-8').split('\n')[0]
        return msg
    return 'OK'
