info=document.getElementById('info');
twt=document.getElementById('twt');
type=document.getElementById('type');
id=document.getElementById('id');
rtbtn=document.getElementById('rtbtn');
upbtn=document.getElementById('upbtn');
resetbtn=document.getElementById('reset');

function getInfo(tid){
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.open('get','/getinfo?id='+tid,false);
  xmlhttp.send();
  return JSON.parse(xmlhttp.responseText);
}

function resetall(){
  info.innerHTML='';
  twt.value='';
  type.value='';
  id.value='';
  rtbtn.type='hidden';
  upbtn.value='Update';
  resetbtn.type='hidden';
  scrollTo(0,0);
}

function re(tid){
  resetall();
  var t=getInfo(tid);
  info.innerHTML='@'+t.name+': '+t.text;
  twt.value='@'+t.name+' '+t.others;
  type.value='re';
  id.value=tid;
  upbtn.value='Reply';
  resetbtn.type='button';
}

function fav(t,tid){
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.open('get','/fav?id='+tid,false);
  xmlhttp.send();
  if(xmlhttp.status==200)
    t.innerHTML=xmlhttp.responseText;
}

function follow(t,name){
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.open('get','/follow?name='+name,false);
  xmlhttp.send();
  if(xmlhttp.status==200)
    t.innerHTML=xmlhttp.responseText;
}


function del(t,tid){
  if(t.innerHTML=='DEL'){
    t.innerHTML='SURE';
  }else{
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.open('get','/del?id='+tid,false);
    xmlhttp.send();
    if(xmlhttp.status==200)
      self.location.reload();
  }
}

function ort(tid){
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.open('get','/ort?id='+tid,false);
  xmlhttp.send();
  if(xmlhttp.status==200)
    self.location='/home';
  else
    info.innerHTML=xmlhttp.responseText;
}

function rt(tid){
  resetall();
  var t=getInfo(tid);
  twt.value='RT @'+t.name+': '+t.text;
  type.value='rt';
  id.value=tid;
  if(!t.protected){
    rtbtn.type='button';
    rtbtn.onclick=function(){ort(tid);};
  }
  upbtn.value='Retweet';
  resetbtn.type='button';
}

function update(){
  form=document.forms[0];
  var params=new Array();
  for(var i=0;i<form.elements.length;i++){
    var p=encodeURIComponent(form.elements[i].name);
    if(!p) continue;
    p+="=";
    p+=encodeURIComponent(form.elements[i].value);
    params.push(p);
  }
  params=params.join("&");
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.open('post','/update',false);
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.setRequestHeader("Content-length", params.length);
  xmlhttp.setRequestHeader("Connection", "close");
  xmlhttp.send(params);
  if(xmlhttp.status==200)
    self.location='/home';
  else
    info.innerHTML=xmlhttp.responseText;
}
// vim:set ts=2 sts=2 sw=2 et sta:
