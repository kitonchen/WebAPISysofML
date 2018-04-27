var w,h,className;
function getSrceenWH(){
	w = $(window).width();
	h = $(window).height();
	$('#dialogBg').width(w).height(h);
}


function addnewtr(data){
    var app = data.app_name;
    var dropid = app+"-drop";
    var deleteid = app+"-delete";
    var type = data.type;
    var api_key = data.api_key;
    var api_sercet = data.api_secret;
    //生成一行
    var $tr = $("<tr id='"+app+"'>"+
    "<td>"+app+"</td>"+
    "<td>"+api_key+"</td>"+
    "<td>"+api_sercet+"</td>"+
    "<td><span class='am-badge am-badge-success'>"+0+"</span></td>"+
    "<td>"+
              "<div class='am-dropdown' data-am-dropdown id='"+dropid+"'>"+
                "<button class='am-btn am-btn-default am-btn-xs am-dropdown-toggle' data-am-dropdown-toggle><span class='am-icon-cog'></span> <span class='am-icon-caret-down'></span></button>"+
                "<ul class='am-dropdown-content'>"+
                  "<li><a href='#' id='"+deleteid+"'>1. 删除</a></li>"+
                "</ul>"+
              "</div>"+
            "</td>"+
               "</tr>");
    $('#keytable tbody').append($tr);
    $("#"+dropid+"").dropdown();
    //绑定点击删除事件
    $("a[id='"+deleteid+"']").click(function(){
        return deletetr($tr,app);
    });
}

function deletetr(trobj,app){
        var flag = window.confirm("您确定要删除该key吗？");
         if(!flag){
          return false;
         } else {
            $.post(
                "/deletekey",
                {appname:app},
                function(data){
                    if(data.status=="success"){
                        trobj.remove();
                    }else{
                        alert("删除失败,请联系管理员");
                    }
                });
          return false;
         }
        return false;
}

window.onresize = function(){
	getSrceenWH();
}  
$(window).resize();  

$(function(){
	getSrceenWH();
	
	//显示弹框
	$('.box a').click(function(){
		className = $(this).attr('class');
		$('#dialogBg').fadeIn(300);
		$('#dialog').removeAttr('class').addClass('animated '+className+'').fadeIn();
	});
	
	//关闭弹窗
	$('.claseDialogBtn').click(function(){
		$('#dialogBg').fadeOut(300,function(){
			$('#dialog').addClass('bounceOutUp').fadeOut();
		});
	});

//生成Key表单验证
	$("#editForm").validate({
	    debug:true,
		rules:{
			appname:{
				required:true,//必填
				minlength:3, //最少6个字符
				maxlength:32,//最多20个字符
				remote:{
					url:"http://localhost:12480/appcheck",//用户名重复检查，别跨域调用
					type:"post"
				}
			},
			apptype:{
			    required:true,
			    minlength:2,
			    maxlength:32
			}
		},
		//错误信息提示
		messages:{
			appname:{
				required:"必须填写应用名",
				minlength:"应用名至少为3个字符",
				maxlength:"应用名至多为32个字符",
				remote: "应用名已存在"
			},
			apptype:{
			    required:"必须填写应用类型",
			    minlength:"类型名称至少为2个字符",
			    maxlength:"类型名称至多为32个字符"
			}
		},
	});

    $('#submit').click(function(){
        var flag = $('#editForm').valid();
        if(!flag){//未通过验证
            return ;
        }
            $.post(
            "/createkey",
            $('#editForm').serialize(),
            function(data){
                addnewtr(data);
                //关闭弹窗
                $('#dialogBg').fadeOut(300,function(){
			    $('#dialog').addClass('bounceOutUp').fadeOut();});
		    });
    });

    $(window).load(function(){
        $.get(
         "/getapikey",
         function(data){
            if(data.status=="success"){
               for(var i in data.keys){
                    addnewtr(JSON.parse(data.keys[i]));
               }
            }else{
                alert("查询失败，请联系管理员");
            }
         }
        )
    });
});

