%# vim: set ts=2 sts=2 sw=2 et sta:
% for user in users:
<div class='userinfo'>
% if defined('simple'):
  <img src='{{user.profile_image_url}}'/><br/>
% else:
  <img src='{{user.profile_image_url.replace('normal.','bigger.')}}'/><br/>
% end
  <b>name</b>: {{user.name}}<br/>
  <b>screen name</b>: <a href='user?name={{user.screen_name}}'>{{user.screen_name}}</a><br/>
% if not defined('simple'):
  <b>is following me</b>: {{is_following_me}}<br/>
% end
  <b>following</b>: <a href='##' onclick='follow(this,"{{user.screen_name}}")'>{{'unfollow' if user.following else 'follow'}}</a><br/>
% import datetime
  <b>created at</b>: {{str(user.created_at+datetime.timedelta(hours=+8))[:10]}}<br/>
  <b>description</b>: {{!user.description}}<br/>
% if user.url:
  <b>url</b>: {{!user.url}}<br/>
% end
  <b>tweets</b>: {{user.statuses_count}}<br/>
  <b>favorites</b>: <a href='/favs?name={{user.screen_name}}'>{{user.favourites_count}}</a><br/>
  <b>following</b>: <a href='following?name={{user.screen_name}}'>{{user.friends_count}}</a><br/>
  <b>followers</b>: <a href='followers?name={{user.screen_name}}'>{{user.followers_count}}</a><br/>
% if not defined('simple'):
  %#<b>lists</b>: <a href='/list?owner={{user.screen_name}}'>{{len(user.lists())}}</a><br/>
  <a href='/list?owner={{user.screen_name}}'>Lists</a><br/>
% end
  <a href='dm?name={{user.screen_name}}'>Direct message</a><br/>
  <a href='listmanage?name={{user.screen_name}}'>Add to lists</a><br/>
</div>
% end
