%# vim: set ts=2 sts=2 sw=2 et sta:
% if tweets:
<ul class='nav even-2' id='pages'>
% prefix = base + ('?' if '?' not in base else '&')
% since_id = tweets[0]['RT_oldId'] if 'RT_oldId' in tweets[0] else tweets[0]['id'] 
% max_id = tweets[-1]['RT_oldId'] if 'RT_oldId' in tweets[-1] else tweets[-1]['id'] 
<li><a href='/{{prefix}}since_id={{since_id}}'>{{'|<<'}}</a></li>
<li><a href='/{{prefix}}max_id={{max_id}}'>{{'>>>'}}</a></li>
</ul>
% end
