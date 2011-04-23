/*
 * echotube - make a youtube radio based on echonest
 * 
 * @author kurtjx (kurt at echonest.com)
 * 
 * for youtube search see http://tikku.com/jquery-jqtube-util#jqtube_tutorial_4
 */


// global player obj
var player = null;
jQTubeUtil.init({key:"AI39si7Sinx6YJqIqFHcd-v2JffS7qWnWz0VZutlrxVKgQm8fhYdMdQV8u-zISSZDOtxO-EIXI8OW8kBi9mkQ4EyuBOAxbdDxQ",
                 maxResults: 1,
                 orderby: "viewCount"});

$(document).ready(
    function(){


    });


var logging = 1;
var host = "developer.echonest.com";
var sessionID = null;
var sessionSeed = null;

var std_params = "?api_key=3YDUQHGT9ZVUBFBR0" +
        "&format=jsonp" +
        "&callback=?" ;
 
var json_params = "?api_key=3YDUQHGT9ZVUBFBR0&format=json";
 
var std_playlist_params = std_params + 
        //"&dmca=true" +
        //"&lookahead=3" +
        //"&bucket=audio_summary" +
        //"&bucket=song_hotttnesss" +
        //"&bucket=artist_hotttnesss" +
        //"&bucket=artist_familiarity" +
        //"&bucket=tracks" +
        //"&limit=true"; 
    "";
 
function fetchArtistPlaylist(artist) {
    info("Found " + artist.name + ". Creating a playlist of tracks by similar sounding artists.");
    var url ="http://" + host + "/api/v4/playlist/dynamic" + std_playlist_params;
    log(url);
 
    var minHotttnesss = artist.hotttnesss;//Math.min(getTaste(), artist.hotttnesss);
 
    setSessionSeedInfo("Artist playlist with seed artist " + artist.name);
    $.getJSON(url, {"artist_id":artist.id, 
                    //"bucket" : "id:" + catalog,
                    "variety" : "0.5", //getVariety(), 
                    "artist_min_hotttnesss": minHotttnesss,
                    "type": "artist-radio"}, function(data) {
            clearInfo();
            sessionID = data.response.session_id;
            if (checkResponse(data)) {
                processSongs(data.response.songs);
            } 
        });
}

function songToYoutubeQuery(song){
    var query = song.artist_name + " " + song.title;
    return query;
}

function processSongs(songs) {
    // search youtube
    for(i in songs){
        log(songs[i]);
        addSongToPlaylist(songs[i]) ;        
    }
}

function newArtistPlaylist() {
    //clearSession();
    var artist_name = sanitize($("#artist_name").val());
 
    if (jQuery.trim(artist_name).length == 0) {
        error("You have to enter an artist name first.");
        return;
    }
 
    info("Searching for " + artist_name);
    var url ="http://" + host + "/api/v4/playlist/dynamic" + std_playlist_params;
    log(url);
    $.getJSON(url, {"artist": artist_name,
                    "type": "artist-radio"}, function(data) {
            if (checkResponse(data)) {
                if(data.response.songs.length > 0){
                    sessionID = data.response.session_id;
                    var playlist = { 
                        title: artist_name,
                        videos: [] 
                    };
                    for(i in data.response.songs){
                        var query = songToYoutubeQuery(data.response.songs[i]);
                        log(query);
                        jQTubeUtil.search(query, function(response){
                                              log(response);
                                              for(v in response.videos){
                                                  var video = {
                                                      id: response.videos[v].videoId ,
                                                      title: response.videos[v].title
                                                  };      
                                                  playlist.videos.push(video);
                                              }
                                              var config =  {
                                                  "chromeless": 0,
                                                  "autoPlay": 1,
                                                  "playlist": playlist
                                              };
                                              player = $('.youtube-player').player(config);
                                              addAnotherSong();
                                          });
                    }
                    log(playlist);
                    
                }
                else{
                    error("No songs found");
                    }
            } 
        });
}

function addAnotherSong(){
    if(sessionID != null){
        var url = "http://" + host + "/api/v4/playlist/dynamic" + std_playlist_params;
        $.getJSON(url, {session_id: sessionID}, function(data){
                      if(checkResponse(data)){
                          var query = songToYoutubeQuery(data.response.songs[0]);
                          jQTubeUtil.search(query, function(response){
                              for(v in response.videos){
                                  var video = {
                                      id: response.videos[v].videoId,
                                      title: response.videos[v].title
                                      };
                             
                                  player.player('loadVideo', video, true);
                              }
                          });
                      }
                  });
    }
}

// Performs basic error checking on the return response from the JSONP call
function checkResponse(data) {
    if (data.response) {
        if (data.response.status.code != 0) {
            error("Whoops... Unexpected error from server. " + data.response.status.message);
            log(JSON.stringify(data.response));
        } else {
            return true;
        }
    } else {
        error("Unexpected response from server");
    }
    return false;
}

// try to avoid html/json injects
function sanitize(s) {
    s = s.replace(/[<>&]/g, "");
    return s;
}

function objLength(obj) {
    var size = 0;
    for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
            size++;
        }
    }
    return size;
}

 
// Shows an error message
function error(msg) {
    info_message(msg, "error_style");
}
 
// shows an info message
function info(msg) {
    info_message(msg, "info_style");
}
 
// shows a message for a few seconds, the
// deletes it
function temp_info(msg, secs) {
    if (!secs) {
        secs = 5;
    }
    setTimeout('clearInfo()', secs * 1000);
    info_message(msg, "info_style");
}
 
// shows a debug mesasge
function debug(msg) {
    if (debugging) {
        warn(msg);
    }
}
 
// baseline styled message 
function info_message(msg, style) {
    clearInfo();
    $("#info_list").append('<span class="' + style + '">' +  msg + '</span>');
}
 
// clear any messages
function clearInfo() {
    $("#info_list").empty();
}
 
// shows a warning message
function warn(msg) {
    info_message(msg, "warn_style");
}
 
// shows a log message
function log(msg) {
    if (logging) {
        console.log(msg);
    }
}

// Creates a new artist playlist
function setSessionSeedInfo(txt) {
    sessionSeed = txt;
}