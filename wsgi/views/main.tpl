%# vim: set ft=html ts=2 sts=2 sw=2 et sta:
%include header title='UglyTwT2',no_nav=True,no_enterbox=True
<h1> welcome to UglyTwT2 !</h1>

<p>Account for sign up and login <b>ONLY</b> means this site <b>NOT</b> Twitter.</p>
<p>After first login, you are required to <b>oauth</b> via Twitter on PC.</p>
<p>Then you are free on mobile.</p>

<form method='POST' id='login'>
  <h2>Login</h2>
  %if defined('error_login') and error_login:
    <p style='color:red'>incorrect username/password</p>
  %end
  <p>
    <input type='hidden' name='type' value='login'/>
    <label>username:</label>
    <input type='text' name='username'/>
  </p>
  <p>
    <label>password:</label>
    <input type='password' name='password'/>
  </p>
  <p><input type='submit' value='login' /></p>
</form>

<form method='POST' id='signup'>
  <h2>Sign up</h2>
  %if defined('error_signup') and error_signup:
    <p style='color:red'>username already exists</p>
  %end
  <p>
    <input type='hidden' name='type' value='signup'/>
    <label>username:</label>
    <input type='text' name='username'/>
  </p>
    <p><label>password:</label>
    <input type='password' name='password'/>
  </p>
  <p><input type='submit' value='sign up' /></p>
</form>
%include footer
