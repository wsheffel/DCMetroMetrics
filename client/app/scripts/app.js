'use strict';

/**
 * @ngdoc overview
 * @name dcmetrometrics
 * @description
 * # dcmetrometrics
 *
 * Main module of the application.
 */
angular
  .module('dcmetrometricsApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'mgcrea.ngStrap'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/home', {
        templateUrl: 'views/main.html',
        controller: 'OutagesCtrl'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl'
      })
      .when('/outages', {
        templateUrl: 'views/outages.html',
        controller: 'OutagesCtrl'
      })
      .when('/stations', {
        templateUrl: 'views/stationlisting.html',
        controller: 'StationDirectoryCtrl'
      })
      .when('/stations/:station', {
        templateUrl: 'views/station.html',
        controller: 'StationCtrl'
      })
      .when('/units/:unitId', {
        templateUrl: 'views/unit.html',
        controller: 'UnitCtrl'
      })
      .otherwise({
        redirectTo: '/home'
      });
  });
