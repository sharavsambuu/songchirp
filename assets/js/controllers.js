/*angular.module("songchirp",[]).
	factory("autoplayService", function($timeout){
		var time = {};
		(function tick() {
			time.now = new Date().toString();
			$timeout(tick, 1000);
		})();
		return time;
	});*/


function CreateCtrl($scope, $http, $location) {
	musicInstance = null;
	shouldPlayMusic = true;
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
			$location.path('/music/'+data[0]["id"]);
		});
	}

	$scope.searchMusic = function() {
		var xsrf = {
			searchValue: $scope.searchText,
		};
		$http({
		    method: 'POST',
		    url: 'searchMusic',
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
			//$scope.searchText = "";
			//console.log(data);
		});
	}

	$scope.generateMusicQueue = function(){
		$http({
		    method: 'POST',
		    url: 'generateMusicQueue'
		}).success(function (data) {
		});		
	}
}

function MusicCtrl($scope, $http) {
	musicInstance = null;
	shouldPlayMusic = true;
	$scope.musicList = [];
	$http.get('getMusicList').success(function(data){
		$scope.musicList = data;
	});
}

function MusicViewCtrl($scope, $routeParams, $http, $timeout, $location) {
	$scope.isLoading = true;
	$scope.progress = 0;

	musicInstance = null;
	shouldPlayMusic = true;

	$scope.onTimeout = function() {
		
		if (shouldPlayMusic) {
			if (musicInstance) {
				var temp = musicInstance.duration();
				if (temp && !isNaN(temp)) {
					if (temp>0) {
						console.log("we need to play music...");
						musicInstance.play();
						shouldPlayMusic = false;			
					}
				}
			}
		}
		if (musicInstance) {
			duration = musicInstance.duration();
			currentTime = musicInstance.currentTime();
			if (!isNaN(duration) && !isNaN(currentTime)){
				$scope.progress = Math.floor((currentTime * 100)/duration);
				if (currentTime>0) {
					$scope.isLoading = false;
				}
				if (duration>0&&(duration-currentTime)<0.5) {
					$location.path('/next');
				}
			}
		}
		//document.getElementById("debug").innerHTML = currentTime+" : "+duration
		
		myTimeout = $timeout($scope.onTimeout, 1500);
	}
	var myTimeout = $timeout($scope.onTimeout, 1500);
	$scope.stopTimout = function() {
		$timeout.cancel(myTimeout);
	}

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

	$scope.boolYoutube    = true;
	$scope.boolVimeo      = true;
	$scope.boolSoundcloud = true;
	$scope.boolMp3        = true;

	$scope.startYoutube = function(source) {
		if ($scope.boolYoutube===true){
			musicInstance = null;
			musicInstance = Popcorn.youtube("#youtubeMusic", source);
			$scope.boolYoutube = false;
			return;
		}
	}
	$scope.startVimeo = function(source) {
		if ($scope.boolVimeo===true){
			musicInstance = null;
			musicInstance = Popcorn.vimeo("#vimeoMusic", source);
			$scope.boolVimeo = false;
			return;
		}	
	}
	$scope.startSoundcloud = function(source) {
		if ($scope.boolSoundcloud===true){
			musicInstance = null;
			musicInstance = Popcorn.soundcloud("#soundcloudMusic",
				source.replace("https", "http")
			);
			$scope.boolSoundcloud = false;
			return;
		}
	}
	$scope.startMp3 = function() {
		if ($scope.boolMp3===true){
			musicInstance = null;
			musicInstance = Popcorn.smart("#mp3Music");
			$scope.boolMp3 = false;
			return;
		}
	}
}
function MusicDeleteCtrl($scope, $routeParams, $http, $location) {
	musicInstance = null;
	shouldPlayMusic = true;
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
	musicInstance = null;
	shouldPlayMusic = true;
	if (musicQueue.length==0) {
		$http({
		    method: 'GET',
		    url: 'getRandomMusicQueue'
		}).success(function (data) {
			//$location.path('/music/'+data[0]["id"]);
			var arr = data[0]["music_list"];
			if (arr) {
				for (var i=0; i<arr.length; i++) {
					musicQueue.push(arr[i]);
				}	
			}
			var musicId = musicQueue.pop();
			console.log("queue length : "+musicQueue.length);
			console.log("history length : "+playHistory.length);
			console.log("selected music id :"+musicId);
			playHistory.push(musicId);
			$location.path('/music/'+Number(musicId));
		});		
	} else {
		var musicId = musicQueue.pop();
		console.log("queue length : "+musicQueue.length);
		console.log("history length : "+playHistory.length);
		console.log("selected music id :"+musicId);
		playHistory.push(musicId);
		$location.path('/music/'+Number(musicId));
	}
}
function MusicViewNextCtrl($scope, $http, $location) {
	$scope.nextMusic = function(){
		musicInstance = null;
		shouldPlayMusic = true;
		$http({
		    method: 'GET',
		    url: 'nextMusic'
		}).success(function (data) {
			$location.path('/music/'+data[0]["id"]);
		});		
	}
}

function MusicBrokenCtrl($scope, $http) {
	$scope.brokenReportCount = 0;
	$scope.report = function(musicId) {
		var xsrf = {
			id: musicId
		};
		$http({
		    method: 'POST',
		    url: 'reportBrokenMusic',
		    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		    transformRequest: function(obj) {
		        var str = [];
		        for(var p in obj)
		        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
		        return str.join("&");
		    },
		    data: xsrf
		}).success(function (data) {
			$scope.brokenReportCount = Number(data[0]["report_count"]);
		});
	}
}

function AboutCtrl($scope) {
}
