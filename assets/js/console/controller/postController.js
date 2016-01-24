/**
 * Posts Controller
 *
 * @author victor li
 * @date 2016/01/21
 */

'use strict';

const Angular = require('angular');

module.exports = Angular.module('PostControllerModule', [])
.controller('PostController', function($scope, $http, $sce) {

    // 控制文章目录下拉框显示状态
    $scope.categoryDropdownShow = false;
    $scope.displayCategoryDropdown = function() {
        $scope.categoryDropdownShow = true;
    };

    $scope.posts = [];
    $scope.fetchPosts = function() {
        const url = '/api/posts';
        $http.get(url).success(function(res) {
            if (res && res.success) {
                $scope.posts = res.data.posts;
                for (let post of $scope.posts) {
                    if (post.summary) {
                        post.summary = $sce.trustAsHtml(post.summary);
                    }
                }
            }
        });
    };

    $scope.fetchPosts();

});

