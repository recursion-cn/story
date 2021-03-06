/**
 * app entry
 *
 * @author victor li
 * @date 2015/11/01
 */

'use strict'

require('expose?$!expose?jQuery!jquery');

const navigatorJudge = function() {
    if (document.documentMode) {
        return 'IE' + document.documentMode;
    }
    return 'Modern';
};

const getPaginationParams = function() {
    const page = $('#js-load-more').data('page');
    const pageSize = $('#js-load-more').data('size');

    return {page: page, pageSize: pageSize};
};

const pagination = function(page, pageSize) {
    const offset = (page - 1) * pageSize;
    const url = '/api/posts?offset=' + offset + '&size=' + pageSize;
    $.get(url, res => {
        if (res && res.data && res.data.posts) {
            const posts = res.data.posts;
            dataBind(posts);
            showOrHidePagination(res.data.need_pagination);
        }
    });
};

const dataBind = function(posts) {
    let fragment = document.createDocumentFragment();
    for (let i = 0, len = posts.length; i < len; i++) {
        let template = $($('#js-post-template').html());
        const item = posts[i];
        template.find('.title-link').attr('href', '/posts/' + item.id).find('p').text(item.title);
        //template.find('.author').attr('href', '/users/' + item.author.id).text(item.author.nick);
        //template.find('.text-info').text(item.last_modified);
        template.find('.post-body').text(item.summary);
        fragment.appendChild(template.get(0));
    }

    const currentPage = $('#js-load-more').data('page');
    $('#js-load-more').data('page', currentPage + 1);

    $(fragment).insertBefore('.post-pagination');
};

const showOrHidePagination = function(bol) {
    if (!bol) {
        $('#js-load-more').parent().hide();
    }
};

const init = function() {
};

$(function() {
    init();
});

$('body').on('click', '.nav-user-panel', (e) => {
    e.stopPropagation();
    $('.nav-user-panel').find('.user-panel').fadeIn()
}).on('click', 'div:not(.user-panel-body)', (e) => {
    $('.nav-user-panel').find('.user-panel').fadeOut()
}).on('click', '#js-load-more', (e) => {
    const params = getPaginationParams()
    const page = params.page + 1;
    pagination(page, params.pageSize)
});
