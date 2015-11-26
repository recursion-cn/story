/**
 * editor module
 * @author victor li
 * @date 2015/11/03
 */

'use strict'

require('expose?$!expose?jQuery!jquery');
require('bootstrap');
const Utils = require('./utils.js');
const referer = $('input[name="referer"]').val();

const init = function() {
    initMarkdownEditor();
};

const initMarkdownEditor = function() {
    const converter = new Markdown.Converter();
    const safeConverter = Markdown.getSanitizingConverter();
    const editor = new Markdown.Editor(safeConverter);
    editor.run();
};

const getPost = function() {
    let post = {};
    post.category = $('input[name="category"]').val();
    post.title = $('input[name="title"]').val();
    post.content = $('textarea[name="content"]').val();
    post.privacy = $('input[name="privacy"]').val();
    post.id = $('input[name="id"]').val();

    return post;
};

const validatePost = function(post) {
    let validate = {valid: true};
    for (let key in post) {
        let value = post[key];
        if (key !== 'privacy' && (!value || !$.trim(value))) {
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

const submitPost = function(post, asDraft) {
    const url = '/posts/create';
    $.post(url, post, function(data) {
        if (data.success) {
            let successTip = '文章发布成功';
            if (asDraft) successTip = '已经保存为草稿';
            Utils.showMsg('success', successTip);
            setTimeout(function() {
                window.location.href = referer;
            }, 3000);
            //window.location.href = referer;
        } else {
            let failedTip = 'Oops，文章发布失败了，喝杯咖啡再试一下';
            if (asDraft) failedTip = 'Oops，草稿保存失败了，喝杯咖啡再试一下';
            Utils.showMsg(failedTip);
        }
    });
};

const initCreateCatePopover = function() {
    const template = '<div class="popover new-cate-popover" role="tooltip"><div class="arrow"></div><div class="popover-title"></div><div class="popover-content"></div></div>';
    const content = '<div class="form-group">'
                    + '<div class="input-group">'
                    + '<div class="input-group-addon">目录名称</div>'
                    + '<input type="text" name="new-cate" class="form-control input-sm"/>'
                    + '<span class="glyphicon glyphicon-ok form-control-feedback" aria-hidden="true"></span>'
                    + '</div></div>'
                    + '<div class="form-group clearfix">'
                    + '<div class="pull-right">'
                    + '<!--button class="btn btn-warning btn-sm" id="js-new-cate-btn-hide">取消</button-->'
                    + '<button class="btn btn-main btn-sm">添加</button>'
                    + '</div>';
    $('#js-add-cate').popover({html: true, template: template, title: '添加目录', content: content});
};

$(function() {
    init();
    initCreateCatePopover();
    window.editorChanged = false;
});

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
        editorChanged = false;
    } else {
        Utils.showMsg('error', validateResult.msg);
    }
}).on('click', '.draft-btn', function(e) {
    // 存为草稿
    e.preventDefault();
    const validateResult = validatePost(getPost());
    if (validateResult.valid) {
        validateResult.data.draft = 1;
        submitPost(validateResult.data, true);
        editorChanged = false;
    } else {
        Utils.showMsg('error', validateResult.msg);
    }
}).on('click', '#js-select-cate>button', function() {
    // 选择文章目录
    $('#js-select-cate>button').removeClass('btn-info').addClass('btn-default');
    $(this).addClass('btn-info');
    const categoryId = $(this).data('id');
    $('input[name="category"]').val(categoryId);
}).on('click', '#js-select-privacy button', function() {
    // 选择是否公开发布
    $('#js-select-privacy button').removeClass('btn-danger').addClass('btn-default');
    const value = $(this).data('value');
    $(this).addClass('btn-danger');
    $('input[name="privacy"]').val(value);
}).on('click', '#js-add-cate', function() {
    // todo
}).on('click', '#js-new-cate-btn-hide', function() {
    $('#js-add-cate')
}).on('input', 'input[name="title"]', function() {
    editorChanged = true;
}).on('input', 'textarea', function() {
    editorChanged = true;
    console.log(editorChanged);
});

$(window).on('beforeunload', function(e) {
    if (editorChanged) {
        return '您有未保存的编辑内容';
    }
}).on('scroll', function() {
    //
});
