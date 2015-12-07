/**
 * setting module
 *
 * @author victor li
 * @date 2015/11/29
 */

'use strict'

const ErrorCode = require('json!./error_code.json');
const Utils = require('./utils.js');

const getPasswordModifyData = function() {
    const oldPassword = $('#js-password-setting input[name="old_password"]').val();
    const newPassword = $('#js-password-setting input[name="new_password"]').val();
    const newPasswordConfirm = $('#js-password-setting input[name="new_password_confirm"]').val();

    return {
        old_password: $.trim(oldPassword),
        new_password: $.trim(newPassword),
        new_password_confirm: $.trim(newPasswordConfirm)
    }
};

const validatePasswordModifyData = function(data) {
    let validateResult = {pass: true};
    if (data) {
        if (!data.old_password) {
            validateResult.pass = false;
            validateResult.msg = '请输入旧密码';
            return validateResult;
        }
        if (data.old_password.indexOf(data.new_password) > -1) {
            validateResult.pass = false;
            validateResult.msg = '新密码不能包含旧密码';
            return validateResult;
        }
        if (!data.new_password || data.new_password.length < 6 || data.new_password.length > 18) {
            validateResult.pass = false;
            validateResult.msg = '请输入6～18位新密码';
            return validateResult;
        }
        if (data.new_password !== data.new_password_confirm) {
            validateResult.pass = false;
            validateResult.msg = '您两次输入的新密码不一致，请再次确认';
            return validateResult;
        }
        validateResult.data = data;
        return validateResult;
    }

    validateResult.pass = false;
    return validateResult;
};

const logout = function() {
    window.location.href = '/users/exit';
};

const changePassword = function(data) {
    const url = '/api/users/change_password';
    $.post(url, data, function(res) {
        if (res && res.success) {
            Utils.showMsg('success', '密码修改成功，请重新登录');
            setTimeout(function() {
                logout();
            }, 1000);
        } else if (!res.success) {
            Utils.showMsg('error', ErrorCode[res.error_code])
        }
    });
};

const deleteCategories = function(data) {
    const url = '/api/category/delete';
    const deletedCates = $('.cate-btn[data-selected=1]');
    $.post(url, data, function(res) {
        if (res && res.success) {
            Utils.showMsg('success', '目录已经删除');
            deletedCates.remove();
        }
    });
};

let _categories = [];

$('body').on('click', '#js-submit-password', function(e) {
    e.preventDefault();
    const validatedPasswordModifyData = validatePasswordModifyData(getPasswordModifyData());
    if (validatedPasswordModifyData.pass) {
        const passwordModifyData = validatedPasswordModifyData.data;
        changePassword(passwordModifyData);
    } else {
        Utils.showMsg('error', validatedPasswordModifyData.msg);
    }
}).on('click', '.cate-btn', function() {
    const id = $(this).data('id');
    if ($(this).data('cate-selected')) {
        const _index = _categories.indexOf(id);
        delete _categories[_index];
        $(this).addClass('btn-default').removeClass('btn-danger').attr('data-selected', 0).data('cate-selected', false);
    } else {
        if (_categories.indexOf(id) < 0) {
            _categories.push(id);
        }
        $(this).addClass('btn-danger').removeClass('btn-default').attr('data-selected', 1).data('cate-selected', true);
    }
}).on('click', '#js-delete-cate', function(e) {
    e.preventDefault();
    let dirtyCategories = [];
    _categories.forEach(function(item) {
        if (item || item === 0) {
            dirtyCategories.push(item);
        }
    });
    if (dirtyCategories.length === 0) {
        Utils.showMsg('error', '请选择要删除的目录');
        return;
    }
    const categoriesStr = dirtyCategories.join(',');
    const data = {'categories': categoriesStr};
    deleteCategories(data);
});

