import bottle
from utils import *
from oauth import *
from libs import *

@bottle.route('/home')
def home():
    if not get_session(): bottle.redirect('/')
    if not get_auth(): bottle.redirect('/oauth')
    tweets = api('home_timeline', **bottle.request.GET)
    tweets = map(process_tweet, tweets)
    return bottle.template('home', tweets=tweets)
