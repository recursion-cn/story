/**
 * Posts Service
 *
 * @author victor li
 * @date 2016/01/25
 */

'use strict';

const Angular = require('angular');

module.exports = Angular.module('PostServiceModule', [])
.service('postService', function($http) {

    return {
        fetchPosts: function(currentPage=1, pageSize=10) {
            const offset = (currentPage - 1) * pageSize;
            const url = `/api/posts?size=${pageSize}&offset=${offset}`;
            return $http.get(url);
        }
    };

});
