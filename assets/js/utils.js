/**
 * Utils module
 *
 * @author victor li
 * @date 2015/10/11
 */

'use strict'

require('expose?$!expose?jQuery!jquery');

let Utils = {};

let cookie = {};

/**
 * add a new cookie
 * @param key value key/name
 * @param value cookie's value
 */
cookie.addCookie = function(key, value, expiresHours) {
    const cookieStr = key + '=' + value;
    let now = new Date();
    if (expiresHours > 0) {
        now.setTime(now.getTime() + expiresHours * 60 * 60 * 1000);
    }
    document.cookie = cookieStr + ';expires=' + now.toGMTString() + ';path=/';
};

/**
 * send ajax with defered
 * @param
 */
Utils.ajax = function(url, data, method) {
    let dfd = $.Deferred();
    let queryParams = '?';
    if (method === 'GET') {
        let i = 0;
        let prefix = '';
        for (const d in data) {
            if (i !== 0) prefix += '&';
            queryParams += (prefix + d + '=' + data[d]);
            i++;
        }
    }
    return $.ajax({
        url: url,
        data: data,
        method: method,
        success: function(data) {
            return dfd.resolve(data);
        },
        error: function(err) {
            return dfd.reject(err)
        }
    });
};

/**
 * show error/warning/sucess message on page
 */
Utils.showMsg = function(type, msg, timeout) {
    if (!timeout) timeout = 6000;
    let selector = '#js-msg-area>.msg-area.success-msg';
    switch (type) {
        case 'error': selector = '.msg-area.error-msg'; break;
        case 'warning': selector = '.msg-area.warning-msg'; break;
        default: selector = '.msg-area.success-msg'; break;
    }

    let msgBar = $(selector);
    let msgArea = msgBar.find('strong');
    msgArea.html(msg);
    msgBar.fadeIn();
    let id = setTimeout(function() {
        msgBar.fadeOut();
        clearTimeout(id);
    }, timeout);
};

Utils.cookie = cookie;

module.exports = Utils;

