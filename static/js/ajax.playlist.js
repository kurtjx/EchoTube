var playlists = [];

$(document).ready(function(){

/*		    $.getJSON("/playlist",
			      {"description": "funky", "artist": "James Brown"},
			      function(playlists){
				$("#player").player({
						      playlists: playlists,
						      updateHash: 1,
						      repeat: 1
						    });
			      });
		    */
		    $("#new_playlist").submit(function(){
						$(this).ajaxSubmit({
								     beforeSubmit: waiting,
								     dataType: 'json',
								     success: resetPlayer
								   });
						return false;
					      });


		  });

function resetPlayer(new_playlist) {
  playlists.push(new_playlist);
  $("#player").player({
			playlists: playlists,
			updateHash: 1,
			repeat: 1
		      });
}

function waiting(){
  $("#player-playlists").html('');
  $("#player").html('<div id="player-video"><div id="player-object">building playlist...<br/><br/><img src="/s/img/player_spinner.gif" alt="waiting"/></div></div>'
			   );
  return true;
}