angular
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
    .controller('menuCtrl', ['$scope', '$http', 'lStorage', function ($scope, $http, lStorage) {
        $scope.trips = lStorage.getAll('trips')
        

        
        $http({
            url: 'http://nettverkkrs.no:5000/buss',
            method: 'POST',
            data: $scope.trips[$scope.trips.length -1],
            headers: {
                'Content-Type': 'application/json'
            }
        }).success(function (data, status, headers, config) {
            $scope.tripps = data;
            console.log('Success')
            console.log($scope.tripps);
                
        }).error(function (data, status, headers, config) {
            $scope.status = status;
            console.log(data, status, headers, config)
        })
        
        
    
        
        /*$scope.uniqueTripps = $scope.tripps.filter(function (item, pos, self) {
            return self.indexOf(item) == pos;
            console.log($scope.uniqueTripps)
        })*/
    


        $scope.sendTrip = function (trip) {
            var newTrip = {
                fra: trip.fra,
                to: trip.to,
                time: trip.time,
                date: trip.date,
                type: trip.type,
                direction: "1"
                
            }
            trip.from = '';
            trip.to = '';
            trip.time = '';
            trip.date = '';
            trip.direction = '';
            $scope.trips.push(newTrip)
            lStorage.save('trips', $scope.trips) = JSON.stringify('trips')
            $scope.trips = lStorage.getAll('trips')
        }

       /* $http({
            method: 'GET',
            url: 'http://nettverkkrs.no:5000/buss',
            params: $rootScope.testTrip,
        }).success(function (data) {
            $scope.trip = data;
            console.log(data)
        }) */
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