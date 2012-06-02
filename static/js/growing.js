$(document).ready(function() {
    $('.nav.pull-right').hide();
    $('#login-form').hide();
    $('#trends-top').attr('class', ''); 
    $('#search-top').attr('class', '');
    $('#growing-top').attr('class', 'active');
});
	
$(document).ready(function() {

	var c = new Date();
	c.setFullYear(2012, 3, 7);
	c.setHours(0);
	c.setMinutes(0);
	c.setSeconds(0);
	c.setMilliseconds(0);
	
	var e=Date();
	var f=(Date.parse(e)-Date.parse(c))/1000;
	var g=Math.floor(f/(3600*24));
	f=f%(3600*24);
	var b=Math.floor(f/3600);
	if(b<10){
	    b="0"+b
	}
	f=f%3600;
	var d=Math.floor(f/60);
	if(d<10){
	    d="0"+d
	}
	f=f%60;
	if(f<10){
	    f="0"+f
	}   
	
	$('#counter').flipify({
    	startTime: g+'天'+b+'小时'+d+'分钟'+f+'秒'
 	});
});

