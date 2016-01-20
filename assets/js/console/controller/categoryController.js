/**
 * Category controller
 *
 * @author victor li
 * @date 2016/01/21
 */

const Angular = require('angular');
const CategoryControllerModule = Angular.module('CategoryControllerModule', []);

CategoryControllerModule.controller('CategoryController', function($scope, $http) {
    $scope.categories = [];
    $http.get('/api/category/list').success(function(res) {
        if (res && res.data) {
            $scope.categories = res.data;
        }
    });
});

module.exports = CategoryControllerModule;
