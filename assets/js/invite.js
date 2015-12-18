/**
 * invite module
 *
 * @author victor li
 * @date 2015/11/29
 */

'use strict'

const ErrorCode = require('json!./error_code.json');
const Utils = require('./utils.js');

const init = function() {
    initInviteHelpPopover();
};

const initInviteHelpPopover = function() {
    $('.invite-help').popover();
};

const getInviteCode = function() {
    const url = '/api/invite/code';
    $.get(url, res => {
        if (res && res.success && res.data) {
            $('.invite-code').text(res.data);
        }
    });
};

$(function() {
    init();
});

$('body').on('click', '.send-invite', function(e) {
    e.preventDefault();
    $('.invite-code').fadeIn();
}).on('click', '#js-get-invite-code', function(e) {
    e.preventDefault();
    getInviteCode();
});