import bottle
from utils import *
from oauth import *
from libs import *

######### function about user ################

@bottle.route('/follow')
def follow():
    ''' ajax function for (un)follow action '''
    if not get_session(): bottle.abort('401')
    if not get_auth(): bottle.abort('401')
    name = bottle.request.GET.get('name','')
    if not name: bottle.abort('401')
    try:
        user = api('get_user', screen_name=name)
        if user.following:
            user.unfollow()
            result='follow'
        else:
            user.follow()
            result='unfollow'
        return result
    except tweepy.TweepError,e:
        bottle.response.status=206
        msg = e.reason.encode('utf-8').split('\n')[0]
        return msg

# why not one function ? #TODO

@bottle.route('/following')
@require_login_oauth
def following():
    ''' people that you are following page '''
    name = bottle.request.GET.get('name','')
    if not name: bottle.redirect('/')
    bottle.request.GET.pop('name')
    if 'cursor' not in bottle.request.GET:
        bottle.request.GET['cursor'] = -1
    result = api('friends', screen_name=name, count=20, **bottle.request.GET)
    return bottle.template('follow', title='following', name=name, users=map(process_user_entities, result[0]), cursor=result[1])

@bottle.route('/followers')
@require_login_oauth
def followers():
    ''' your followers page '''
    name = bottle.request.GET.get('name','')
    if not name: bottle.redirect('/')
    bottle.request.GET.pop('name')
    if 'cursor' not in bottle.request.GET:
        bottle.request.GET['cursor'] = -1
    result = api('followers', screen_name=name, count=20, **bottle.request.GET)
    return bottle.template('follow', title='followers', name=name, users=map(process_user_entities, result[0]), cursor=result[1])

@bottle.route('/user')
@require_login_oauth
def user():
    ''' user info page '''
    name = bottle.request.GET.get('name','')
    if not name: bottle.redirect('/')
    bottle.request.GET.pop('name')
    try:
        tweets = api('user_timeline', screen_name=name, **bottle.request.GET)
        tweets = process_tweets(tweets)
    except:
        tweets = None
    #is_following_me = api('exists_friendship', user_a=name, user_b=get_user_db().screen_name)
    is_following_me = api('show_friendship', source_screen_name=name, target_screen_name=get_user_db().screen_name)[0].following
    user = api('get_user', screen_name=name)
    user = process_user_entities(user)
    return bottle.template('user', user=user, tweets=tweets, is_following_me=is_following_me)
