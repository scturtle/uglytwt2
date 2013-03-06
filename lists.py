import bottle
from utils import *
from oauth import *
from libs import *

@bottle.route('/listm')
def follow():
    ''' ajax function for list managment '''
    if not get_session(): bottle.abort('401')
    if not get_auth(): bottle.abort('401')
    name = bottle.request.GET.get('name','')
    list_id = bottle.request.GET.get('list_id','')
    action = bottle.request.GET.get('action','')
    if action=='add':
        api('add_list_member', list_id=list_id, screen_name=name)
    else:
        api('remove_list_member', list_id=list_id, screen_name=name)
    return 'OK'

@bottle.route('/listmanage')
@require_login_oauth
def listmanage():
    name = bottle.request.GET.get('name','')
    me = api('me')
    lists = me.lists()
    result = []
    for l in lists:
        if l.user.screen_name != me.screen_name:
            continue
        try:
            is_member = l.is_member(name)
        except:
            is_member = False
        result.append([l, is_member])
    return bottle.template('listmanage', title='list manage', name=name, result=result)

@bottle.route('/listmember')
@require_login_oauth
def listmember():
    ''' members of list '''
    owner = bottle.request.GET.get('owner','')
    slug = bottle.request.GET.get('slug','')
    cursor = bottle.request.GET.get('cursor','-1')
    result = api('list_members', owner_screen_name=owner, slug=slug, cursor=cursor, count=20)
    return bottle.template('listmember', title='members', owner=owner, slug=slug, users=result[0], cursor=result[1])


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
        for l in user.lists(): #+user.lists_subscriptions():
            slugs.append([l.full_name[1:].split("/")[0],l.slug,l.full_name])
        return bottle.template('lists', only_slugs=True, owner=user.screen_name, slugs=slugs)
    else:
        try:
            bottle.request.GET.pop('owner')
            bottle.request.GET.pop('slug')
        except:pass
        tweets = api('list_timeline', owner_screen_name=user.screen_name, slug=slug, **bottle.request.GET)
        tweets = process_tweets(tweets)
        return bottle.template('lists', only_slugs=False, owner=user.screen_name, slug=slug, tweets=tweets)
