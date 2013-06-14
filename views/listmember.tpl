%# vim: set ts=2 sts=2 sw=2 et sta:
%include header title=title,no_enterbox=True
<p><b>List members of <a href='/list?owner={{owner}}&slug={{slug}}'>
{{owner}}/{{slug}}</a>:</b></p>
%include userinfo users=users,simple=True
<ul class='nav even-2' id='pages'>
<li><a href='/listmember?owner={{owner}}&slug={{slug}}&cursor={{cursor[0] if cursor[0]!=0 else -1}}'>{{'<<<'}}</a></li>
<li><a href='/listmember?owner={{owner}}&slug={{slug}}&cursor={{cursor[1]}}'>{{'>>>'}}</a></li>
</div>
%include footer
