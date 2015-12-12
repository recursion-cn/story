/**
 * editor module
 * @author victor li
 * @date 2015/11/03
 */

'use strict'

const Utils = require('./utils.js');
const referer = $('input[name="referer"]').val();
let editor;

const init = function() {
    initMarkdownEditor();
};

const initMarkdownEditor = function() {
    const md = $('#js-post-content').html() || '';
    editor = editormd('js-editormd', {
        path: '/assets/lib/editor.md/lib/',
        markdown: md,
        autoLoadModules: false,
        saveHTMLToTextarea: true,
        //tex: true,
        tocm: true,
        emoji: true,
        taskList: true,
        codeFold: true,
        searchReplace: true,
        htmlDecode: "style, script, iframe",
        flowChart: true,
        sequenceDiagram: true
    })
};

const getPost = function() {
    let post = {};
    post.category = $('input[name="category"]').val();
    post.title = $('input[name="title"]').val();
    post.content = editor.getMarkdown();
    post.privacy = $('input[name="privacy"]').val();
    post.id = $('input[name="id"]').val();
console.log(post)
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
            if (!asDraft) {
                setTimeout(function() {
                    window.location.href = referer;
                }, 3000);
            }
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
                    + '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>'
                    + '</div></div>'
                    + '<div class="form-group clearfix">'
                    + '<div class="pull-left cate-msg-area"></div>'
                    + '<div class="pull-right">'
                    + '<!--button class="btn btn-warning btn-sm" id="js-new-cate-btn-hide">取消</button-->'
                    + '<button class="btn btn-main btn-sm js-btn-add-cate">添加</button>'
                    + '</div>';
    $('#js-add-cate').popover({html: true, template: template, title: '添加目录', content: content});
};

const getInputCategory = function() {
    return $('input[name="new-cate"]').val();
};

const addCategory = function(data) {
    const url = '/category/add';
    const inputElement = $('input[name="new-cate"]');
    $.post(url, data, function(res) {
        if (res && res.success) {
            addCategoryElement(res.category_id, data.cate_name);
            $('#js-add-cate').popover('hide');
        } else if (!res.success) {
            // TODO
            inputElement.closest('.form-group').addClass('has-error');
            inputElement.next().removeClass('glyphicon-ok').addClass('glyphicon-remove');
        }
    });
};

const addCategoryElement = function(cate_id, cate_name) {
    const element = $('<button class="btn btn-default btn-sm"></button>');
    element.attr('data-id', cate_id).text(cate_name);
    $('#js-select-cate').append(element);
};

const categoryExist = function(data) {
    const url = '/category/exist';
    const inputElement = $('input[name="new-cate"]');
    $.get(url, data, function(res) {
        if (res && res.success) {
            if (res.exist) {
                inputElement.closest('.form-group').addClass('has-error').removeClass('has-success');
                inputElement.next().removeClass('glyphicon-ok').addClass('glyphicon-remove');
                inputElement.closest('.popover').find('.cate-msg-area').html('<span class="text-danger">目录已经存在了</span>');
            } else {
                inputElement.closest('.form-group').addClass('has-success').removeClass('has-error');
                inputElement.next().removeClass('glyphicon-remove').addClass('glyphicon-ok');
                inputElement.closest('.popover').find('.cate-msg-area').html('');
            }
        } else if (!res.success) {
            // TODO
            inputElement.closest('.form-group').addClass('has-error').removeClass('has-success');
            inputElement.next().removeClass('glyphicon-ok').addClass('glyphicon-remove');
            inputElement.closest('.popover').find('.cate-msg-area').html('<span class="text-danger">Oops，数据请求异常</span>');
        }
    });
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
}).on('click', '.js-btn-add-cate', function() {
    const cate = getInputCategory();
    if ('' === $.trim(cate)) return;
    const data = {cate_name: cate};
    addCategory(data);
}).on('input', 'input[name="new-cate"]', function() {
    clearTimeout(timer);
    timer = setTimeout(function() {
        const cate = getInputCategory();
        if ('' === $.trim(cate)) return;
        const data = {cate_name: cate};
        categoryExist(data);
    }, 300);
});

let timer;

$(window).on('beforeunload', function(e) {
    if (editorChanged) {
        return '您有未保存的编辑内容';
    }
}).on('scroll', function() {
    //
});
