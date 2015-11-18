/**
 * editor module
 * @author victor li
 * @date 2015/11/03
 */

'use strict'

require('expose?$!expose?jQuery!jquery');
const converter = new Markdown.Converter();
const safeConverter = Markdown.getSanitizingConverter();
const editor = new Markdown.Editor(safeConverter);
editor.run();
const Utils = require('./utils.js');
const referer = $('input[name="referer"]').val();

const getPost = function() {
    let post = {};
    post.category = $('select[name="category"]').val();
    post.title = $('input[name="title"]').val();
    post.content = $('textarea[name="content"]').val();
    post._public = $('input[name="public"]:checked').val();
    post.id = $('input[name="id"]').val();

    return post;
};

const validatePost = function(post) {
    let validate = {valid: true};
    for (let key in post) {
        let value = post[key];
        if (key !== '_public' && (!value || !$.trim(value))) {
            validate.valid = false;
            validate.msg = key + '不允许为空';
            return validate;
        }
        if (key === 'title' && key.length > 100) {
            validate.valid = false;
            validate.msg = '标题超过100个字符';
            return validate;
        }
    }
    validate.data = post;

    return validate;
};

const submitPost = function(post) {
    const url = '/posts/create';
    $.post(url, post, function(data) {
        if (data.success) {
            Utils.showMsg('success', '文章发布成功');
            setTimeout(function() {
                window.location.href = referer;
            }, 2000);
            //window.location.href = referer;
        } else {
            Utils.showMsg('发布失败，请稍候试一试吧');
        }
    });
};

$('body').on('click', '.switch-editor-mode', function(e) {
    const mode = $(this).data('mode');
    $('.switch-editor-mode').removeClass('active');
    $(this).addClass('active');
    if (mode === 'edit') {
        $('.editor-preview').hide();
        $('.editor-area').show();
    } else if (mode === 'preview') {
        $('.editor-area').hide();
        $('.editor-preview').show();
    }
}).on('click', '.submit-btn', function(e) {
    // 立即发布
    e.preventDefault();
    const validateResult = validatePost(getPost());
    if (validateResult.valid) {
        validateResult.data.draft = 0;
        submitPost(validateResult.data);
    } else {
        Utils.showMsg('error', validateResult.msg);
    }
}).on('click', '.draft-btn', function(e) {
    // 存为草稿
    e.preventDefault();
    const validateResult = validatePost(getPost());
    if (validateResult.valid) {
        validateResult.data.draft = 1;
        submitPost(validateResult.data);
    } else {
        Utils.showMsg('error', validateResult.msg);
    }
});
