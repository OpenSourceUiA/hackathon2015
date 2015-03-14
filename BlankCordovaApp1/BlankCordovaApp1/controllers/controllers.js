﻿angular
    .module('app.controllers', ['ionic'])
    .controller('homeCtrl', ['$scope', 'lStorage', function ($scope, lStorage) {
        $scope.previousTrips = lStorage.getAll('trips');
        $scope.deleteTrip = function (idx) {
            $scope.previousTrips.splice(idx, 1);
        }

        $scope.toggleTrip = function (trip) {
            if ($scope.isTripShown(trip)) {
                $scope.shownTrip = null;
            } else {
                $scope.shownTrip = trip;
            }
        };
        $scope.isTripShown = function (trip) {
            return $scope.shownTrip === trip;
        };

    }])
    .controller('menuCtrl', ['$scope', 'lStorage', function ($scope, lStorage) {
        $scope.trips = lStorage.getAll('trips')

        $scope.sendTrip = function (trip) {
            var newTrip = {
                from: trip.from,
                to: trip.to,
                time: trip.time,
                date: trip.date,
                type: trip.type
            }
            trip.from = '';
            trip.to = '';
            trip.time = '';
            trip.date = '';
            $scope.trips.push(newTrip)
            lStorage.save('trips', $scope.trips)
        }
        function menuToggle($scope, $ionicSideMenuDelegate) {
            $scope.toggleLeft = function () {
                $ionicSideMenuDelegate.toggleLeft();
            };
        }
    }])
    .factory('lStorage', function () {
        var getAll = function (key) {
            var itemString = window.localStorage.getItem(key)
            if (itemString) {
                var items = JSON.parse(itemString)
                return items
            }
            return [];
        };
        var save = function (key, item) {
            var itemString = JSON.stringify(item)
            window.localStorage.setItem(key, itemString)
        };
        return {
            getAll: getAll,
            save: save
        }
    })
;