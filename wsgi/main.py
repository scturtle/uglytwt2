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

#  bottle functions  #############################
@bottle.route('/')
def main():
    if get_session():
        bottle.redirect('/home')
    return bottle.template('main')

@bottle.post('/')
def login_signup():
    if 'username' in bottle.request.POST and 'password' in bottle.request.POST:
        username = bottle.request.POST['username']
        password = bottle.request.POST['password']
        tp = bottle.request.POST['type']
        if tp=='login':
            if username and user_auth(username, password):
                create_session(username)
                bottle.redirect('/home')
            else:
                return bottle.template('main',error_login=True)
        elif tp=='signup':
            if username:
                user = create_user(username, password)
                if user != 'exists':
                    create_session(username)
                    bottle.redirect('/home')
                else:
                    return bottle.template('main',error_signup=True)
    return bottle.template('main')

@bottle.route('/logout')
def logout():
    destroy_session()
    bottle.redirect('/')

@bottle.error(500)
def innerError(error):
    return bottle.template('error',e=error)

@bottle.route('/me')
def me():
    if not get_session(): bottle.redirect('/')
    if not get_auth(): bottle.redirect('/oauth')
    me = api('me')
    return bottle.redirect('/user?name='+me.screen_name)

@bottle.route('/mention')
def mention():
    if not get_session(): bottle.redirect('/')
    if not get_auth(): bottle.redirect('/oauth')
    tweets = api('mentions',**bottle.request.GET)
    tweets = map(process_tweet, tweets)
    return bottle.template('mention', tweets=tweets)

@bottle.route('/favs')
def favs():
    if not get_session(): bottle.redirect('/')
    if not get_auth(): bottle.redirect('/oauth')
    name = bottle.request.GET.get('name','')
    if not name: name=api('me').screen_name
    try:
        bottle.request.GET.pop('name')
    except:pass
    tweets = api('favorites',screen_name=name,**bottle.request.GET)
    tweets = map(process_tweet, tweets)
    return bottle.template('fav', name=name, tweets=tweets)

@bottle.route('/thread')
def thread():
    if not get_session(): bottle.redirect('/')
    if not get_auth(): bottle.redirect('/oauth')
    tweets = [api('get_status',id=bottle.request.GET['id'])]
    while tweets[-1].in_reply_to_status_id:
        tweets.append(api('get_status',id=tweets[-1].in_reply_to_status_id))
    tweets = map(process_tweet, tweets)
    return bottle.template('thread', tweets=tweets)

@bottle.route('/exit')
def _exit():
    if not get_session(): bottle.redirect('/')
    return bottle.template('exit')

import tweepy
@bottle.route('/apitest')
def apitest():
    ''' useful function for test api '''
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
        if type(r) in [tweepy.models.Status, tweepy.models.User]:
            d = {}
            for idx in filter(lambda idx: not idx.startswith('__'), dir(r)):
                d[idx]=getattr(r,idx)
            results[i] = d
    from pprint import pformat
    from cgi import escape
    return '<pre>\n',escape(pformat(results)),'</pre>'


bottle.debug(True)
application = bottle.default_app()
