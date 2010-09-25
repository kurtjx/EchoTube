var playlists = [{title: "kurtjx's picks",
		  videos: [
		    { id: 'EI6iZJOntY8', title: 'Lupe Fiasco - Hurt Me Soul' },
		    { id: 'FDVzaTMF-ps', title: "Alexander O'neal & Cherelle - Saturday luv"}
		    ]
		 }];

$(document).ready(
  function(){
    $("#pl-desc").hide();
    $("input[name=description]").attr('value','').hide();
    $("#form-text").html('Use this form to create a new playlist');
    $("#new_playlist_form").submit(function(){
				     $(this).ajaxSubmit({
						     beforeSubmit: waiting,
						     dataType: 'json',
						     success: resetPlayer
						   });
				     return false;
				   });
    $("select#pl-type").change(function(){
				 if($("#new_playlist_form select[name=type]").val()=="artist-description"){
				   $("#pl-artist").hide();
				   $("input[name=artist]").attr('value','').hide();
				   $("#pl-desc").show();
				   $("input[name=description]").show();
				 }
				 else{
				   $("#pl-desc").hide();
				   $("input[name=description]").attr('value','').hide();
				   $("#pl-artist").show();
				   $("input[name=artist]").show();
				 }
			       });
  });

function resetPlayer(response) {
  $('input').removeAttr("disabled");
  $('select').removeAttr("disabled");
  if(response.success){

    playlists.unshift(response.playlist);
    //console.log(playlists);

    $("#err-text").html('');
    // fix youtube player bug
    $("#player-playlists").remove();
    // clear old player
    $("#player").html('<div id="player-video"><div id="player-object"></div></div>');
    // make new player
    $("#player").player({
			playlists: playlists,
			updateHash: 0,
			repeat: 1
		      });
  }
  else{
    $("#err-text").html('<span id="error">' + response.message + '</span>');
  }

}


function waiting(){
  //$('input[type=submit]').attr('disabled', 'disabled');
  $('input').attr('disabled', 'disabled');
  $('select').attr('disabled','disabled');
  $("#err-text").html('creating playlist, plz be patient <img src="img/player_spinner.gif" alt="waiting"/>');
  return true;
}