%# vim: set ts=2 sts=2 sw=2 et sta:
% if tweets:
<div id='pages'>
% prefix = base + ('?' if '?' not in base else '&')
<a href='/{{prefix}}since_id={{tweets[0]['id']}}'>{{'|<<'}}</a>
<a href='/{{prefix}}max_id={{tweets[-1]['id']}}'>{{'>>>'}}</a>
</div>
% end
