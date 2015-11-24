/**
 * editor module
 * @author victor li
 * @date 2015/11/07
 */

'use strict'

require('expose?$!expose?jQuery!jquery');
require('bootstrap');

const converter = new Markdown.Converter();
const safeConverter = Markdown.getSanitizingConverter();
const Utils = require('./utils.js');

const parseMarkdown = function(md) {
    return safeConverter.makeHtml(md);
};

const renderMarkdown = function(mdHtml) {
    $('#js-content').html(mdHtml);
};

const render = function() {
    const md = $('#js-content-template').html();
    renderMarkdown(parseMarkdown(md));
    $('#js-content-template').remove();
};

//render();

/**
 * find all <img/> tags from post
 */
const findImgs = function() {
    return $('.single-post>.content').find('img');
};

const markImgsZoom = function($imgs) {
    $imgs.each(function(index, item) {
        console.log(item);
    });
};

const deletePost = function(id) {
    $.ajax({
        url: '/posts/delete/' + id,
        type: 'DELETE',
        success: function(result) {
            if (result.success) {
                Utils.showMsg('success', '文章已删除');
            } else {
                Utils.showMsg('error', '文章删除失败，请稍候试一试吧');
            }
        }
    });
};

const initDeleteConfirmTooltip = function() {
    const title = '确实要删除这篇文章吗？';
    const content = '<div class="row" id="js-delete-confirm">'
                    + '<div class="col-md-6">'
                    + '<button class="btn btn-default btn-sm cancel-btn">取消</button>'
                    + '</div>'
                    + '<div class="col-md-6">'
                    + '<button class="btn btn-danger btn-sm sure-btn">确定</button>'
                    + '</div>'
                    + '</div>';
    const template = '<div class="popover" role="tooltip"><div class="popover-title"></div><div class="popover-content"></div></div>';
    $('#js-delete-post').popover({html: true, title: title, content: content});
};

$(function() {
    //initDeleteConfirmTooltip();
});

$('body').on('click', '#js-delete-confirm .cancel-btn', function() {
    //const id = $('#js-delete-post').data('id');
    //deletePost(id);
}).on('click', '#js-delete-post', function() {
    $('#js-delete-confirm-modal').modal({show: true});
}).on('click', '#js-delete-confirm-modal .confirm-btn', function() {
    const id = $('#js-delete-post').data('id');
    deletePost(id);
    $('#js-delete-confirm-modal').modal('hide');
});
