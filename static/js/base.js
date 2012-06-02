$(document).ready(function(){
    if ( $.browser.msie ) {
        var msg = document.createElement("div");
		msg.id = "errorMsg";
		msg.innerHTML = "<div align='center'><h1>月饼(Eric Yue):<br>   求求你不要用IE来折磨我T_T<br><br>推荐Chrome/Safari</h1></div>";

		document.body.appendChild(msg);
		$("#navbar").css("display", "none")
		$("#navbar").css("display", "none")
		$("#navbar").css("display", "none")
		$(".container").css("display", "none")
	    document.execCommand("stop");
     }

});
$(document).ready(function(){
    $("#loginButton").click(function(){
        $.getJSON("login",  
                  { 
                   password:MD5($('#pwd').val()),  
                   email:$('#email').val()
                  },  
                   function(data){  
                   if(data.msg == 'ok'){
                         window.location.href="http://127.0.0.1:8000";
                          
                                    }else{  
                                        $.jGrowl("用户名或密码错误！",{		
                                        					animateOpen:{ 
                                        						height: "show",
                                        						width: "show"
                                        					},life:2000,
                                        					header:"错误",position:"center" 
                                        					}); 
                                    }});
    });
});
$(document).ready(function(){
    $("#login-form").fadeIn(1000);
});
$(document).ready(function(){
	// hide #back-top first
	$("#back-top").hide();
	// fade in #back-top
	$(function () {
		$(window).scroll(function () {
			if ($(this).scrollTop() > 100) {
				$('#back-top').fadeIn();
			} else {
				$('#back-top').fadeOut();
			}
		});
		// scroll body to 0px on click
		$('#back-top a').click(function () {
			$('body,html').animate({
				scrollTop: 0
			}, 800);
			return false;
		});
	});

});
