%# vim: set ts=2 sts=2 sw=2 et sta:
%include header title='Activity',no_enterbox=False
% for act in acts:
<p><b>
% for i in act.sources:
<img src='{{i.profile_image_url.replace('normal', 'mini')}}'>
{{i.name}}(<a href='/user?name={{i.screen_name}}'>@{{i.screen_name}}</a>)
% end
{{act.action}}:</b></p>
% if act.action in ['retweet', 'favorite']:
% include tweets tweets=act.targets
% else:
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
