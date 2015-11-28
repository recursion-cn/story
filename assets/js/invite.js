/**
 * invite module
 *
 * @author victor li
 * @date 2015/11/29
 */

'use strict'

require('expose?$!expose?jQuery!jquery');
const ErrorCode = require('json!./error_code.json');
const Utils = require('./utils.js');

const init = function() {
    initInviteHelpPopover();
};

const initInviteHelpPopover = function() {
    $('.invite-help').popover();
};

$(function() {
    init();
});

$('body').on('click', '.send-invite', function(e) {
    e.preventDefault();
    $('.invite-code').fadeIn();
});