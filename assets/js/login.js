/**
 * login module
 *
 * @author victor li
 * @date 2015/11/06
 */

'use strict'

require('expose?$!expose?jQuery!jquery');
const ErrorCode = require('json!./error_code.json');
const Utils = require('./utils.js');

let getNext = function() {
    const href = location.href;
    let next = '/';
    if (href.indexOf('next=') < 0) {
        return next;
    }
    const hrefArg = href.split('?');
    if (hrefArg.length > 1) {
        const param = hrefArg[1].split('=');
        next = decodeURIComponent(param[1].replace('next', ''));
    }
    return next;
}

/**
 * validate form params
 */
let validate = function(params, showErrorFun) {
    let result = {
        pass: true,
        msg: ''
    };
    for (const k in params) {
        if (k === 'nick') {
            const v = $.trim(params[k]);
            if (!v) {
                result.pass = false;
                result.msg = '用户名不能为空';
                showErrorFun('error', result.msg);
                break;
            }
        }
        if (k === 'password') {
            const v = $.trim(params[k]);
            if (!v || v.length < 6 || v.length > 18) {
                result.pass = false;
                result.msg = '密码长度应介于6到18个字符之间';
                showErrorFun('error', result.msg);
                break;
            }
        }
    }

    if (!result.pass) {
        return result;
    }

    result.params = params;
    return result;
};

/**
 * show error message on page
 */
/**let showError = function(error) {
    let errorMsgArea = $('.error-msg');
    errorMsgArea.html(error).fadeIn();
    let id = setTimeout(function() {
        errorMsgArea.fadeOut();
        clearTimeout(id);
    }, 3000);
};**/

/**
 * hide error message from page
 */
let hideError = function() {
    let errorMsg = $('.error-msg');
    errorMsg.hide();
};

/**
 * execute the login action
 */
let login = function(params) {
    if (!params.pass)
        return;
    const url = '/users/login';
    const next = (getNext());
    $.post(url, params.params, function(data) {
        if (data) {
            if (data.success) {
                const member = data.data;
                //Utils.cookie.addCookie('current_user', member.nick, 7 * 24);
                window.location.href = next;
            } else {
                Utils.showMsg('error', ErrorCode[data.error_code]);
            }
        }
    });
};

let getParams = function() {
    const nick = $('input[name="nick"]').val();
    const password = $('input[name="password"]').val();
    return {
        nick: nick,
        password: password
    }
};

$('body').on('click', 'button.submit', function(e) {
    e.preventDefault();
    hideError();
    login(validate(getParams(), Utils.showMsg));
});

