/**
 * editor module
 * @author victor li
 * @date 2016/01/16
 */

'use strict'

const Utils = require('./utils.js');

// 获取文章目录
function getCategories() {
    $.get('/api/category/list', data => {
        if (data && data.data) {
            const categories = data.data;
            renderCategories(categories);
        }
    })
};

// 渲染文章目录到页面
function renderCategories(categories) {
    let categoriesHtml = '';
    categories.forEach(category => {
        categoriesHtml += `<a class="cate" href="" data-id=${category.id}>${category.name}</a>`;
    });
    $('#js-cates-list').html($(categoriesHtml));
};

function getPosts() {
    $.get('/api/posts/list', data => {
        if (data && data.data) {
            const posts = data.data;
            renderPosts(posts);
        }
    });
};

function renderPosts(posts) {
    let postsHtml = '';
};

getCategories();