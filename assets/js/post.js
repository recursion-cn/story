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