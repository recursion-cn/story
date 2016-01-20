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
const ConsoleApp = Angular.module('ConsoleApp', ['ngRoute',
    'MainControllerModule',
    'CategoryControllerModule'])
/*.config(['$interpolateProvider', function($interpolateProvider) {
    Angular.bootstrap([document.documentElement, function($interpolateProvider) {
        $interpolateProvider.startSymbol('#{');
        $interpolateProvider.endSymbol('}#');
    }]);
}]);
*/
module.exports = ConsoleApp;
