var movieControllers = angular.module('movieControllers', []);

movieControllers.movieControllers('MovieDetailController', ['$scope', '$routeParams', '$http',
	function($scope, $routeParams, $http) {
		$http.get('http://localhost:8001/api/movies/' + $routeParams.movieId + '.json').success(function(data) {
			$scope.movie = data;
		});
	}
])