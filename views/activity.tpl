%# vim: set ts=2 sts=2 sw=2 et sta:
%include header title='Activity',no_enterbox=False
% for act in acts:
<p>
% for i in act.sources:
<img src='{{i.profile_image_url.replace('normal', 'mini')}}'>
<a href='/user?name={{i.screen_name}}'>@{{i.screen_name}}</a><small>({{i.name}})</small>
% end
<b>
% if act.action=='list_member_added':
% l = act.target_objects[0]
add member to list <a href='/list?owner={{l.user.screen_name}}&slug={{l.slug}}'>{{l.full_name}}</a>:
% end
% if act.action=='list_created':
% l = act.targets[0]
create list <a href='/list?owner={{l.user.screen_name}}&slug={{l.slug}}'>{{l.full_name}}</a>
% end
% if not act.action.startswith('list'):
{{act.action}}:
% end
</b></p>
% if act.action in ('retweet', 'favorite'):
% include tweets tweets=act.targets
% end
% if act.action in ('follow', 'list_member_added'):
% include userinfo users=act.targets, simple=True
% end
% end

% if acts:
<ul class='nav even-2' id='pages'>
<li><a href='/activity'>{{'|<<'}}</a></li>
<li><a href='/activity?max_id={{acts[-1].max_position}}'>{{'>>>'}}</a></li>
</ul>
% end

%include footer
