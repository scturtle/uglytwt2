%# vim: set ft=html ts=2 sts=2 sw=2 et sta:
%include header title='Search',no_enterbox=True
<div id='input'>
  <form>
  <input type='text' name='q' value='{{q}}' style='width:100%'><br/>
  not only Chinese<input type='checkbox' name='nozh' value='true' {{'checked' if nozh else ''}}> 
  <input type='submit' value='search'>
</div>
%include tweets tweets=tweets
% base = 'search'
% if q: 
%   base += '?q='+q
%   if nozh:
%     base += '&nozh='+nozh
%   end
% end
%include pages  base=base,tweets=tweets
%include footer
