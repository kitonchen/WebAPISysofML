(function($) {
  'use strict';

  $(function() {
    var $fullText = $('.admin-fullText');
    $('#admin-fullscreen').on('click', function() {
      $.AMUI.fullscreen.toggle();
      $.AMUI.fullscreen.isFullscreen ? $fullText.text('关闭全屏') : $fullText.text('开启全屏');
    });
  });
})(jQuery);

//jquery.validate表单验证
$(document).ready(function(){
    //修改表单验证
	$("#changeForm").validate({
		rules:{
			user-name:{
				required:true,//必填
				minlength:3, //最少6个字符
				maxlength:32,//最多20个字符
				remote:{
					url:"http://localhost:12480/registcheck",//用户名重复检查，别跨域调用
					type:"post"
				}
			},
			user-email:{
				required:true,
				email:true
			},
			user-phone:{
			    required:true,
				phone_number:true,//自定义的规则
				digits:true//整数
			}
		},
		//错误信息提示
		messages:{
			user-name:{
				required:"必须填写用户名",
				minlength:"用户名至少为3个字符",
				maxlength:"用户名至多为32个字符",
				remote: "用户名已存在"
			},
		    user-email:{
				required:"请输入邮箱地址",
				email: "请输入正确的email地址"
			},
			user-phone:{
				required:"请输入手机号码",
				digits:"请输入正确的手机号码"
			}
		}

	});
    //添加自定义验证规则
	jQuery.validator.addMethod("user-phone", function(value, element) {
		var length = value.length;
		var phone_number = /^(((13[0-9]{1})|(15[0-9]{1}))+\d{8})$/
		return this.optional(element) || (length == 11 && phone_number.test(value));
	}, "手机号码格式错误");
});