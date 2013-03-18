/**
* @_prompto
*/

//-------------------globals-------------------------
var musicInstance = null;
var shouldPlayMusic = true;
var duration = 0.0;
var currentTime = 0.0;
var playHistory = [];
var musicQueue = [];

// ------------------functions-----------------------
(function(){
}());

window.onload = function() {
};

// utils
window.requestAnimFrame = (function () {
	return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
	function ( /* function */ callback, /* DOMElement */ element) {
	  window.setTimeout(callback, 1000 / 60);
	};
})();
function youtube_parser(url) {
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
    var match = url.match(regExp);
    if (match&&match[7].length==11){
        return match[7];
    }else{
        return null;
    }
}
<!-- http://stackoverflow.com/questions/3452546/javascript-regex-how-to-get-youtube-video-id-from-url -->
function IDForMedia(pastedData) {
	var success = false;
	var media   = {};
	if (pastedData.match('http://(www.)?youtube|youtu\.be')) {
	    if (pastedData.match('embed')) { youtube_id = pastedData.split(/embed\//)[1].split('"')[0]; }
	    else { youtube_id = pastedData.split(/v\/|v=|youtu\.be\//)[1].split(/[?&]/)[0]; }
	    media.type  = "youtube";
	    media.id    = "http://www.youtube.com/watch?v="+youtube_id;
	    success = true;
	}
	else if (pastedData.match('http://(player.)?vimeo\.com')) {
	    vimeo_id = pastedData.split(/video\/|http:\/\/vimeo\.com\//)[1].split(/[?&]/)[0];
	    media.type  = "vimeo";
	    media.id    = "http://player.vimeo.com/video/"+vimeo_id;
	    success = true;
	}
	else if (pastedData.match('https://(www.)?soundcloud\.com')) {
	    //soundcloud_url = unescape(pastedData.split(/value="/)[1].split(/["]/)[0]);
	    //soundcloud_id = soundcloud_url.split(/tracks\//)[1].split(/[&"]/)[0];
	    media.type  = "soundcloud";
	    media.id    = pastedData;
	    success = true;
	}
	if (success) { return media; }
	else { //alert("No valid media id detected"); 
	}
	return false;
}

function toSoundCloud(url) {
	var temp = url;
	temp = temp.replace(":","%3A");
	temp = temp.replace("https","http");
	return temp.replace("/","%2F");
}

// angularjs template configuration
var app = angular.module('songchirp', []);
    app.config(function($interpolateProvider) {
      $interpolateProvider.startSymbol('[[');
      $interpolateProvider.endSymbol(']]');
});


angular.module('songchirp', []).
config(function($routeProvider) {
	$routeProvider.
		when('/', {controller:MusicCtrl, templateUrl:'templates/music.html'}).
		when('/new', {controller:CreateCtrl, templateUrl:'templates/new.html'}).
		when('/music', {controller:MusicCtrl, templateUrl:'templates/music.html'}).
		when('/music/:id', {controller:MusicViewCtrl, templateUrl:'templates/musicview.html'}).
		when('/music/delete/:id', {controller:MusicDeleteCtrl, templateUrl:'templates/music.html'}).
		when('/next', {controller:MusicNextCtrl, templateUrl:'templates/next.html'}).
		when('/about', {controller:MusicCtrl, templateUrl:'templates/about.html'}).
		otherwise({redirectTo:'/'});
});