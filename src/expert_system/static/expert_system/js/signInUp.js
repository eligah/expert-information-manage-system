/**
 * Created by eligah on 2016/6/13.
 */
// save users' status
sessionStorage.account = "null";
sessionStorage.nickname = "null";

// sign up
$("#btn-sign-up").bind("click", function () {
    checkSignUp();
});
$("#to-sign-in").bind("click", function () {
    $('#signUp').modal('hide');
    $('#signIn').modal('show');
});

//sign in
$("#btn-sign-in").bind("click", function () {
    checkSignIn();
});
$("#to-sign-up").bind("click", function () {
    $('#signIn').modal('hide');
    $('#signUp').modal('show');
});


function checkSignUp() {
    if ($("#sign-up-account").val() == "") {
        $("#sign-up-account")
            .parent()
            .addClass("has-warning");

        $("#sign-up-account")
            .focus()
            .attr("placeholder", "your account is empty");
        return false;
    }
    else {
        if ($("#sign-up-nickname").val() == "") {
            $("#sign-up-nickname")
                .parent()
                .addClass("has-warning");
            $("#sign-up-nickname")
                .focus()
                .attr("placeholder", "your account is empty");
            return false;
        }
        else if ($("#sign-up-password").val() == "") {
            $("#sign-up-password")
                .parent()
                .addClass("has-warning");
            $("#sign-up-password")
                .focus()
                .attr("placeholder", "your passward is empty");
            return false;
        }
        else {
            var signUpInfo = {
                "account": $("#sign-up-account").val(),
                "nickname": $("#sign-up-nickname").val(),
                "password": $("#sign-up-password").val()
            };
            $.ajax({
                url: '',
                type: "POST",
                data: signUpInfo,
                success: function (data) {
                    if (data.status == 300) {
                        $("#sign-up-account")
                            .focus()
                            .attr("placeholder", "your account is dumplicate");
                    }
                    if (data.status == 100) {
                        sessionStorage.account = data.account;
                        sessionStorage.nickname = data.nickname;
                        $('.sign').hide();
                        $(' #user-account').text(sessionStorage.account);
                        $(' #user-nickname').text(sessionStorage.nickname);
                        $('.user-info').show();
                        $('#signUp').modal('hide');
                    }
                }
            });
        }
    }
}

function checkSignIn() {
    if ($("#sign-in-account").val() == "") {
        $("#sign-in-account")
            .parent()
            .addClass("has-warning");

        $("#sign-in-account")
            .focus()
            .attr("placeholder", "your account is empty");
        return false;
    }
    else if ($("#sign-in-password").val() == "") {
        $("#sign-in-password")
            .parent()
            .addClass("has-warning");
        $("#sign-in-password")
            .focus()
            .attr("placeholder", "your passward is empty");
        return false;
    }
    else {
        var signinInfo = {
            "account": $("#sign-in-account").val(),
            "password": $("#sign-in-password").val()
        };
        $.ajax({
            url: '',
            type: "POST",
            data: signinInfo,
            success: function (data) {
                if (data.status == 200) {
                    $("#sign-in-password")
                        .focus()
                        .attr("placeholder", "wrong password");
                }
                else if (data.status == 100) {
                    sessionStorage.account = data.account;
                    sessionStorage.nickname = data.nickname;
                    $('.sign').hide();
                    $(' #user-account').text(sessionStorage.account);
                    $(' #user-nickname').text(sessionStorage.nickname);
                    $('.user-info').show();
                    $('#signIn').modal('hide');
                }
            }
        });
    }
}