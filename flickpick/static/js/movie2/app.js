var movieApp = angular.module('movieApp', ['ngRoute', 'movieControllers']);

movieApp.config(['$routeProvider',
	function($routeProvider){
		$routeProvider.
		when('/movie/:movieId', {
			// templateUrl: DjangoProperties.STATIC_URL + 'movie2/partials/etc.html'
			templateUrl: 'http://localhost:8001/static/js/movie2/partials/movie-detail.html',
			controller: 'movieControllers'
		});
	}
]);

movieApp.config([
	'$httpProvider', function($httpProvider) {
		$httpProvider.defaults.xsrfCookieName = 'csrftoken';
		$httpProvider.defaults.vsrfHeaderName = 'X-CSRFToken';
	}
]);