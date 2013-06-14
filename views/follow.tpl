%# vim: set ts=2 sts=2 sw=2 et sta:
%include header title=title,no_enterbox=True
<p><b>{{(name+' is following') if title=='following' else ('followers of '+name)}}:</b></p>
%include userinfo users=users,simple=True
<ul class='nav even-2' id='pages'>
<li><a href='/{{title}}?name={{name}}&cursor={{cursor[0]}}'>{{'<<<'}}</a></li>
<li><a href='/{{title}}?name={{name}}&cursor={{cursor[1]}}'>{{'>>>'}}</a></li>
</div>
%include footer
