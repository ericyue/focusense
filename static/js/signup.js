
$(document).ready(function(){
    $("#login-form").hide();
});
$(document).ready(function(){
    $("#e-mail").blur(function(){
       var email=$('#e-mail').val();  
       if(email==''||email==null){
           $('#error-empty-email').fadeIn(500);
       }else{
           $('#error-empty-email').fadeOut(500);
       }
    }).click(function(){
        $('#suggestion').fadeOut(500);
    });
});
$(document).ready(function(){
    $("#error-empty-pwd").fadeOut(500);
    $("#passwd").click(function(){
       $("#suggestion-pwd").fadeOut(500);
    }).blur(function(){
        if($("#passwd").val()!=''){
            $("#error-empty-pwd").fadeOut(500);
        }else{
            $("#error-empty-pwd").fadeIn(500);
        }   
    });
    $("#re-passwd").blur(function(){
        var pwd=$('#passwd').val();
        var repwd=$('#re-passwd').val();
           if(pwd!=repwd){
               $("#error-repwd").fadeIn(500);
           }else{
               $("#error-repwd").fadeOut(500);
           }
    });
});
$(document).ready(function(){
    $('.alert-error').hide();
    $('#error-repwd').hide();
    $("#accept-box").click(function(){
        $("#accept-rule").fadeOut(500);  
    });
    $("#submit").click(function(){
        var status=$("#accept-box").attr("checked");
        if(status=="checked"){
            var pwd=$('#passwd').val();
            var em=$('#e-mail').val();
            $.jGrowl("正在提交注册请求...",{		
            					animateOpen:{ 
            						height: "show",
            						width: "show"
            					},life:2000,position:"bottom-right" 
            					});
            					
            $.getJSON("register",  
                      { 
                       password:MD5(pwd),  
                       email:em
                      },  
                       function(data){
                       if(data.msg == 'ok'){
                             window.location.href="http://127.0.0.1:8000"; 
                                        }else{  
                                            $.jGrowl("服务器临时错误,请稍后重试...",{		
                                            					animateOpen:{ 
                                            						height: "show",
                                            						width: "show"
                                            					},life:2000,position:"bottom-right" 
                                            					});  
                                        }});
        }else{
            $("#accept-rule").fadeIn(500);
        }

    });
});