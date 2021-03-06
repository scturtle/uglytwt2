import bottle
from utils import *
from oauth import *
from libs import *

@bottle.route('/home')
@require_login_oauth
def home():
    ''' home timeline page '''
    tweets = api('home_timeline', **bottle.request.GET)
    tweets = process_tweets(tweets)
    return bottle.template('home', tweets=tweets)
