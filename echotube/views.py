from django.shortcuts import render_to_response
from django.http import HttpResponse
from simplejson import dumps

import echonest_calls as echonest
import youtube_calls as youtube


def playlist(request):
    if request.GET:
        descriptions = request.GET.getlist('description')
        artists = request.GET.getlist('artist')
        if len(descriptions)>0:
            title = descriptions[0]
        elif len(artists)>0:
            title = artists[0]
        else:
            title = 'untitled'
        params = {}
        for key,value in request.GET.items():
            if key != 'description' and key != 'artist':
                params.update({key:value})
        enjson = echonest.playlist_description(descriptions, artists, params)
        pljson =  {'title': title , 'videos':[] } 
        for song in enjson:
            query_text = song['artist_name']
            query_text += ' ' + song['title']
            print "searching: "+ query_text + 'type: '+ str(type(query_text))
            vids = youtube.search(query_text)
            if len(vids)>0:
                pljson['videos'].append({'id': vids[0]['id'], 'title':vids[0]['title']})
        return HttpResponse(dumps(pljson), 'application/javascript')
    else:
        return HttpResponse('no data')    
