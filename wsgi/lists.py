import bottle
from utils import *
from oauth import *
from libs import *

@bottle.route('/list')
@require_login_oauth
def lists():
    ''' lists page '''
    owner = bottle.request.GET.get('owner','')
    if not owner:
        user=api('me')
    else:
        user=api('get_user',screen_name=owner)
    slug = bottle.request.GET.get('slug','')
    if not slug:
        slugs=[]
        for l in user.lists()+user.lists_subscriptions():
            slugs.append([l.full_name[1:].split("/")[0],l.slug,l.full_name])
        return bottle.template('lists', only_slugs=True, owner=user.screen_name, slugs=slugs)
    else:
        try:
            bottle.request.GET.pop('owner')
            bottle.request.GET.pop('slug')
        except:pass
        tweets = api('list_timeline', owner=user.screen_name, slug=slug, **bottle.request.GET)
        tweets = map(process_tweet, tweets)
        return bottle.template('lists', only_slugs=False, owner=user.screen_name, slug=slug, tweets=tweets)
