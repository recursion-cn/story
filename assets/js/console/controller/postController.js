/**
 * Posts Controller
 *
 * @author victor li
 * @date 2016/01/21
 */

'use strict';

const Angular = require('angular');
require('../service/postService.js');

module.exports = Angular.module('PostControllerModule', ['PostServiceModule'])
.controller('PostController', function($scope, postService, $sce) {

    // 控制文章目录下拉框显示状态
    $scope.categoryDropdownShow = false;
    $scope.displayCategoryDropdown = function() {
        $scope.categoryDropdownShow = true;
    };

    // 是否显示“加载更多”按钮
    $scope.loadMoreDisplay = false;
    $scope.currentPage = 1;
    $scope.pageSize = 10;

    // 获取文章列表
    $scope.posts = [];
    $scope.fetchPosts = function() {
        postService.fetchPosts($scope.currentPage, $scope.pageSize).success(res => {
            $scope.handleResponse(res, false);
        });
    };

    // 加载更多
    $scope.loadMore = function() {
        postService.fetchPosts(++$scope.currentPage, $scope.pageSize).success(res => {
            $scope.handleResponse(res, true);
        });
    };

    // 处理“获取文章列表”的返回数据
    $scope.handleResponse = function(response, append=false) {
        if (response && response.success) {
            const data = response.data;
            $scope.loadMoreDisplay = data.need_pagination;
            if (append) {
                const morePosts = data.posts;
                for (let post of morePosts) {
                    $scope.posts.push(post);
                }
                return;
            }
            $scope.posts = data.posts;
            $scope.firstPost = $scope.posts[5];
            $scope.firstPost.html = $sce.trustAsHtml($scope.firstPost.html_content);
        }
    };

    $scope.fetchPosts();

});

