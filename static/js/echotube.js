
$(document).ready(
  function(){
    $("#pl-desc").hide();
    $("input[name=description]").attr('value','');
    $("#form-text").html('Use this form to create a new playlist');
    $("#player-playlists").remove();
    
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
				   $("input[name=artist]").attr('value','');
				   $("#pl-desc").show();
				 }
				 else{
				   $("#pl-desc").hide();
				   $("input[name=description]").attr('value','');
				   $("#pl-artist").show();
				 }
			       });

    // add artist / desc stuff
    $("#add-artist").click(function(){
			     $("#pl-artist").append('<label>artist:</label><input id="pl-artist" type="text" name="artist" value="" size="17" placeholder="seed artist for playlist"><br/>');
			   });
    $("#add-desc").click(function(){
			   $("#pl-desc").append('<label>description:</label><input id="pl-desc" type="text" name="description" value="" size="17" placeholder="tags to make a playlist"/><br/>');
			 });
  });

function resetPlayer(response) {
  $('input').removeAttr("disabled");
  $('select').removeAttr("disabled");
  if(response.success){
    //console.log(response.playlist.uri);
    window.location.replace(response.playlist.uri);
    playlists.unshift(response.playlist);
    //console.log(playlists);

    /*$("#err-text").html('');
    // fix youtube player bug
    $("#player-playlists").remove();
    // clear old player
    $("#player").html('<div id="player-video"><div id="player-object"></div></div>');
    // make new player
    $("#player").player({
			playlists: playlists,
			updateHash: 0,
			repeat: 1
		      });*/
  }
  else{
    $("#err-text").html('<span id="error">' + response.message + '</span>');
  }

}


function waiting(){
  //$('input[type=submit]').attr('disabled', 'disabled');
  $('input').attr('disabled', 'disabled');
  $('select').attr('disabled','disabled');
  $("#err-text").html('creating playlist, plz be patient <img src="/img/player_spinner.gif" alt="waiting"/>');
  return true;
}