function HomeCtrl($scope){

}

function CreateCtrl($scope, $http, $location) {
	$scope.musicTypes = [
		"youtube, soundcloud, vimeo",
		"mp3"
	];
	$scope.musicType = $scope.musicTypes[0];
	$scope.musicName = "";
	$scope.musicSource = "";

	$scope.submitMusic = function(){
		if ($scope.musicType!="mp3") {
			var media = IDForMedia($scope.musicSource);
			if (media) {
				$scope.musicType   = media.type;
				$scope.musicSource = media.id;
			}
		}
		var xsrf = {
			type: $scope.musicType,
			name: $scope.musicName,
			source: $scope.musicSource
		};
		$http({
		    method: 'POST',
		    url: 'addMusic',
		    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		    transformRequest: function(obj) {
		        var str = [];
		        for(var p in obj)
		        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
		        return str.join("&");
		    },
		    data: xsrf
		}).success(function (data) {
			$scope.musicType = $scope.musicTypes[0];
			$scope.musicName = "";
			$scope.musicSource = "";
			//console.log(data[0]["id"]);
			$location.path('/music/'+data[0]["id"]);
		});
	}
}

function MusicCtrl($scope, $http) {
	$scope.musicList = [];
	$http.get('getMusicList').success(function(data){
		$scope.musicList = data;
	});
}

function MusicViewCtrl($scope, $routeParams, $http) {
	$scope.musicList = [];
	var xsrf = {
		id: $routeParams.id,
	};
	
	$http({
	    method: 'POST',
	    url: 'getMusic',
	    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
	    transformRequest: function(obj) {
	        var str = [];
	        for(var p in obj)
	        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
	        return str.join("&");
	    },
	    data: xsrf
	}).success(function (data) {
		$scope.musicList = data;
	});
}
function MusicDeleteCtrl($scope, $routeParams, $http, $location) {
	var xsrf = {
		id: $routeParams.id,
	};
	$http({
	    method: 'POST',
	    url: 'deleteMusic',
	    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
	    transformRequest: function(obj) {
	        var str = [];
	        for(var p in obj)
	        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
	        return str.join("&");
	    },
	    data: xsrf
	}).success(function (data) {
		$location.path('/music');
	});
}
function MusicNextCtrl($scope, $http, $location) {
	console.log("next music controller is working");
	alert("it works");
	/*$http({
	    method: 'GET',
	    url: 'nextMusic'
	}).success(function (data) {
		console.log(data[0]["id"])
		//$location.path('/music/'+data[0]["id"]);
	});	*/
}

function AboutCtrl($scope) {
}