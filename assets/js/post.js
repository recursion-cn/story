/**
 * editor module
 * @author victor li
 * @date 2015/11/07
 */

'use strict'

require('expose?$!expose?jQuery!jquery');
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

render();

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

$('body').on('click', '#js-delete-post', function() {
    const id = $(this).data('id');
    deletePost(id);
});
