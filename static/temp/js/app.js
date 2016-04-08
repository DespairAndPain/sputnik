
 'use strict';

var recipeApp = angular.module('marvelApp', [
  'ngRoute',
  'marvelControllers'
]);

recipeApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        // отображение всех рецептов
        templateUrl: 'static/temp/partials/list.html',
        controller: 'ListCtrl'
      });
  }]);

recipeApp.config([
    '$httpProvider', function($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoke',
      $httpProvider.defaults.xsrfCookieName = 'X-CSRFToken'
  }
]);


 console.log(1);