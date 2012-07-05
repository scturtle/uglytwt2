#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *
from oauth import *
from libs import *

import bottle

from home import *
from user import *
from update import *
from lists import *
from dm import *

from google.appengine.api import users

#  bottle functions  #############################

@bottle.route('/')
def index(): # Cannot be main! Fuck you, GAE!
    if get_session():
        bottle.redirect('/home')
    login_url = users.create_login_url('/')
    return bottle.template('main',{'login_url':login_url})

@bottle.route('/logout')
def logout():
    logout_url = users.create_logout_url('/')
    bottle.redirect(logout_url)

@bottle.error(500)
def innerError(error):
    ''' universal error handler page '''
    return bottle.template('error',e=error)

@bottle.route('/me')
@require_login_oauth
def me():
    me = api('me')
    return bottle.redirect('/user?name='+me.screen_name)

@bottle.route('/search')
@require_login_oauth
def search():
    ''' search page '''
    q = bottle.request.GET.get('q','')
    nozh = bottle.request.GET.get('nozh','')
    if q:
        if nozh=='true':
            tweets = api('search',rpp=20,**bottle.request.GET)
        else:
            tweets = api('search',rpp=20,lang='zh',**bottle.request.GET)
    else:
        tweets=[]
    tweets = process_tweets(tweets)
    return bottle.template('search', tweets=tweets, q=q, nozh=nozh)


@bottle.route('/mention')
@require_login_oauth
def mention():
    ''' mentions(replies) of me '''
    tweets = api('mentions',**bottle.request.GET)
    tweets = process_tweets(tweets)
    return bottle.template('mention', tweets=tweets)

@bottle.route('/favs')
@require_login_oauth
def favs():
    ''' favorite tweets of me or others '''
    name = bottle.request.GET.get('name','')
    if not name: name=api('me').screen_name
    try:
        bottle.request.GET.pop('name')
    except:pass
    tweets = api('favorites',screen_name=name,**bottle.request.GET)
    tweets = process_tweets(tweets)
    return bottle.template('fav', name=name, tweets=tweets)

@bottle.route('/thread')
@require_login_oauth
def thread():
    ''' thread of replies '''
    tweets = [api('get_status',id=bottle.request.GET['id'])]
    while tweets[-1].in_reply_to_status_id:
        tweets.append(api('get_status',id=tweets[-1].in_reply_to_status_id))
    tweets = process_tweets(tweets)
    return bottle.template('thread', tweets=tweets)

@bottle.route('/exit')
def _exit():
    if not get_session(): bottle.redirect('/')
    return bottle.template('exit')

import tweepy
@bottle.route('/apitest')
def apitest():
    ''' useful function for test api !!! '''
    if not get_session(): bottle.redirect('/')
    auth = get_auth()
    if not auth: bottle.redirect('/oauth')

    gets = bottle.request.GET
    if 'method' not in gets:
        bottle.abort(401, 'no method paramater')
    method = getattr(tweepy.API(auth), gets['method'], None)
    if not method:
        bottle.abort(401, 'no method paramater')
    del gets['method']
    results = method(**gets)
    if not hasattr(results,'__iter__'):
        results = [results]
    for i,r in enumerate(results):
        if type(r) in [tweepy.models.SearchResult, tweepy.models.DirectMessage,
                tweepy.models.Status, tweepy.models.User]:
            d = {}
            for idx in filter(lambda idx: not idx.startswith('__'), dir(r)):
                d[idx]=getattr(r,idx)
            results[i] = d
    from pprint import pformat
    from cgi import escape
    return '<pre>\n',escape(pformat(results)),'</pre>'


if __name__=='__main__':
    bottle.debug(True)
    bottle.run(server='gae')