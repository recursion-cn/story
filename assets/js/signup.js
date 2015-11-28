/**
 * login module
 *
 * @author victor li
 * @date 2015/11/28
 */

'use strict'

require('expose?$!expose?jQuery!jquery');
const ErrorCode = require('json!./error_code.json');
const Utils = require('./utils.js');

const getRegisterInfo = function() {
    const nick = $('input[name="nick"]').val();
    const password = $('input[name="password"]').val();
    const password_confirm = $('input[name="password_confirm"]').val();
    const invite_code = $('input[name="invite_code"]').val();

    return {
        nick: $.trim(nick),
        password: $.trim(password),
        password_confirm: $.trim(password_confirm),
        invite_code: $.trim(invite_code)
    };
};

const validateRegisterInfo = function(info) {
    let validateResult = {pass: true};
    if (info) {
        if (!info.nick || info.nick.length > 6) {
            validateResult.pass = false;
            validateResult.msg = '请输入6个字符以内的昵称';
            return validateResult;
        }
        if (!info.password || info.password.length > 18 || info.password < 6) {
            validateResult.pass = false;
            validateResult.msg = '请输入6-18位密码';
            return validateResult;
        }
        if (info.password_confirm !== info.password) {
            validateResult.pass = false;
            validateResult.msg = '两次密码输入不一致';
            return validateResult;
        }
        if (!info.invite_code) {
            validateResult.pass = false;
            validateResult.msg = '请输入邀请码';
            return validateResult;
        }
        validateResult.data = info;
    }

    return validateResult;
};

const signup = function(data) {
    const url = '/users/signup';
    $.post(url, data, function(res) {
        if (res && res.success) {
            Utils.showMsg('success', '注册成功，3秒后将跳转到登录页面');
            setTimeout(function() {
                window.location.href = '/users/login';
            }, 3000);
        } else if (!res.success) {
            Utils.showMsg('error', ErrorCode[res.error_code]);
        }
    });
};

$('body').on('click', '.submit', function(e) {
    e.preventDefault();
    const validatedRegisterInfo = validateRegisterInfo(getRegisterInfo());
    if (validatedRegisterInfo.pass) {
        const registerInfo = validatedRegisterInfo.data;
        signup(registerInfo);
    } else {
        Utils.showMsg('error', validatedRegisterInfo.msg);
    }
});
