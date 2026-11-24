(function(){
var K='b12ns',h=document.documentElement,b=document.getElementById('nsw');
if(!b)return;
function set(on){h.classList.toggle('ns',on);b.setAttribute('aria-checked',on?'true':'false');}
set(h.classList.contains('ns'));
b.addEventListener('click',function(){
 var on=!h.classList.contains('ns');set(on);
 try{localStorage.setItem(K,on?'1':'0');}catch(e){}
 try{if(window.gtag)gtag('event','no_spoilers',{action:on?'on':'off',page:location.pathname});}catch(e){}
});
})();
