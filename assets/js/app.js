/**
 * app entry
 *
 * @author victor li
 * @date 2015/11/01
 */

'use strict'

require('expose?$!expose?jQuery!jquery');

const getPaginationParams = function() {
    const offset = $('#js-load-more').data('offset');
    const size = $('#js-load-more').data('size');

    return {offset: offset, size: size};
};

const pagination = function(offset, size) {
    const url = '/api/posts?offset=' + offset + '&size=' + size;
    $.get(url, res => {
        if (res) {
            const data = JSON.parse(res.data);
            dataBind(data);
        }
    });
};

const dataBind = function(data) {
    let fragment = document.createDocumentFragment();
    for (let i = 0, len = data.length; i < len; i++) {
        let template = $($('#js-post-template').html());
        const item = data[i];
        template.find('.title').attr('href', '/posts/' + item.id).find('h3').text(item.title);
        template.find('.author').attr('href', '/users/' + item.author.id).text(item.author.nick);
        template.find('.text-info').text(item.last_modified);
        template.find('.post-body').text(item.summary);
        fragment.appendChild(template.get(0));
    }

    $(fragment).insertBefore('.post-pagination');
};

$('body').on('mouseover', '.nav-user-panel', e =>
    $(this).find('.user-panel').fadeIn()
).on('mouseleave', '.nav-user-panel', e =>
    $(this).find('.user-panel').fadeOut()
).on('click', '#js-load-more', e => {
    const params = getPaginationParams()
    pagination(params.offset, params.size)
});
