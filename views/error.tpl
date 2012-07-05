%# vim: set ft=html ts=2 sts=2 sw=2 et sta:
%include header title='Error',no_nav=True,no_enterbox=True
<div style='text-align:center;font-size:64px'>囧rz</div>
<p>{{e.status}} {{e.output}}:</p>
<p><b>{{e.exception.reason if hasattr(e.exception,'reason') else e.exception.message}}</b></p>
<p>If this happens all the time, try to <a href='/unoauth'>unoauth</a> and oauth again.</p>
<small style='font-size:10px'>{{e.traceback}}</small>
%include footer
