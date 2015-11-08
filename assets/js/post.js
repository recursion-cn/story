/**
 * editor module
 * @author victor li
 * @date 2015/11/07
 */

'use strict'

require('expose?$!expose?jQuery!jquery');

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
            console.log(result);
        }
    });
};

$('body').on('click', '#js-delete-post', function() {
    const id = $(this).data('id');
    deletePost(id);
});
