import bottle
from utils import *
from oauth import *
from libs import *

########## some function for ajax ############

@bottle.route('/getinfo')
def getinfo():
    ''' get infomation for one tweet '''
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
    ''' offical retweet '''
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
    ''' favorite action '''
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
    ''' delete tweet or dm '''
    if not get_session(): bottle.abort('401')
    if not get_auth(): bottle.abort('401')
    tp = bottle.request.GET.get('type',None)
    try:
        if not tp:
            tweet = api('destroy_status', id=bottle.request.GET['id'])
        elif tp=='dm':
            tweet = api('destroy_direct_message', id=bottle.request.GET['id'])
    except tweepy.TweepError,e:
        bottle.response.status=206
        msg = e.reason.encode('utf-8').split('\n')[0]
        return msg
    return 'OK'

@bottle.post('/update')
def update():
    ''' update tweet, reply, rt or dm '''
    if not get_session(): bottle.abort('401')
    if not get_auth(): bottle.abort('401')
    tp=bottle.request.POST.get('type',None)
    try:
        if not tp:
            api('update_status',status=bottle.request.POST['twt'],
                    in_reply_to_status_id=bottle.request.POST['id'])
        elif tp=='dm':
            api('send_direct_message',text=bottle.request.POST['msg'],
                    user=bottle.request.POST['name'].lstrip('@'))
            return bottle.redirect('/dm?type=byme')
    except tweepy.TweepError,e:
        bottle.response.status=206
        msg = e.reason.encode('utf-8').split('\n')[0]
        return msg
    return 'OK'
