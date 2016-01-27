/**
 * app
 *
 * @author victor li
 * @date 2016/01/20
 */

'use strict';

const Angular = require('angular');
const ngRoute = require('angular-route');

const MainControllerModule = require('./controller/mainController.js');
const CategoryControllerModule = require('./controller/categoryController.js');
const PostControllerModule = require('./controller/postController.js');

const ConsoleApp = Angular.module('ConsoleApp',
    [
        'ngRoute',
        'MainControllerModule',
        'CategoryControllerModule',
        'PostControllerModule',
        'lumx'
    ],
    function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    });

// route define
ConsoleApp.config(['$routeProvider', function ($routeProvider) {
      $routeProvider
      .when('/posts', {
          templateUrl: '/assets/templates/posts.html',
          controller: 'PostController'
      })
      .when('/drafts', {
          templateUrl: '/assets/templates/posts.html',
          controller: 'PostController'
      })
      .when('/post/:id', {
          templateUrl: '/assets/templates/posts.html',
          controller: 'PostController'
      })
      .otherwise({
        redirectTo: '/posts'
      });
}])

module.exports = ConsoleApp;

