function bindEmailCaptchaClick() {
    $("#captcha-btn").click(function (event) {
        var $this = $(this)

        event.preventDefault();

        var username = $("#username").val()
        var password = $("#password").val()
        var password2 = $("#password2").val()
        var email = $("input[name='email']").val();
        var phone = $("#phone").val()
        var address = $("#address").val()
        var data = {
            "username": username,
            "password": password,
            "password2": password2,
            "email": email,
            "phone": phone,
            "address": address
        }
        $.ajax({
            url: "/auth/captcha/email?email=" + email,
            type: "POST",
            method: "GET",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: function (result) {
                var code = result.code;
                if (code == 200) {
                    var timer = countdown = 5;
                    // 将按钮设置为不可点击
                    $this.attr("disabled", "disabled");
                    setInterval(function () {
                        $this.text('请稍等...' + countdown);
                        countdown--;
                        // 倒计时结束之后
                        if (countdown <= 0) {
                            clearInterval(timer);
                            // 将按钮的初始文本内容恢复
                            $this.text("获取验证码");
                            // 将按钮设置为可点击
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                    // alert("验证码发送成功");
                } else {
                    alert("验证码发送失败");
                    }
                },
            fail: function (error) {
                console.log(error);
            }
        })
    })
}


$(function () {
    bindEmailCaptchaClick();
})