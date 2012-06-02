/* Like Button Ajax
 * =============== */
$(document).ready(function(){
    $('#like-button').click(function(){
        $.getJSON("../like",  
                  { 
                   pid:$(this).attr('value'),  
                  },  
                   function(data){  
                   if(data.msg == 'ok'){
                        $.jGrowl(" 我们收到您的“喜欢” ^ ^ ",{		
                        					animateOpen:{ 
                        						height: "show",
                        						width: "show"
                        					},life:2000,
                        					header:"通知中心",position:"bottom-right" 
                        					});
                        					
                   }else{  
                        alert(data.msg);  
        }});
    });
});

$(document).ready(function() {
    $(".fancybox").fancybox({
    				padding: 0,

    				openEffect : 'elastic',
    				openSpeed  : 150,
    				closeEffect : 'elastic',
    				closeSpeed  : 150,
    				closeClick : true,
    				maxHeight:400,
    				maxWidth:500,
    				helpers : {
    				    
    					overlay : {
                        						speedIn : 500,
                                                opacity : 0.6
                        					}
    				}
    			});
});

$(document).ready(function() {
    $(".dislike-recommend").click(function(){
        $(this).parent().parent().parent().fadeOut(500); 
    });
    $("#commen_taobao").lionbars();
    $("#standardSelector").click(function(){
        $.getJSON("../share",  
                  { 
                   pid:$(this).attr('value'),  
                  },  
                   function(data){  
                   if(data.msg == 'ok'){
                        
                   }else{  
                        alert(data.msg);  
        }});
    });
});


