from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from simplejson import dumps

import echonest_calls as echonest
import youtube_calls as youtube


def api(request):
    if request.GET:
        descriptions = request.GET.getlist('description')
        artists = request.GET.getlist('artist')
        terms = request.GET.getlist('term')
        if len(descriptions)>0 and descriptions[0]!='':
            title = descriptions[0]
        elif len(artists)>0:
            title = artists[0]
        else:
            title = 'untitled'
        print 'title is: '+title
        params = {}
        for key,value in request.GET.items():
            if key != 'description' and key != 'artist' and key!='term' and value !='':
                params.update({key:value})
        try:
            enjson = echonest.playlist_description(descriptions, artists, params)
        except echonest.EchonestAPIException as e:
            return HttpResponse(dumps({'success':False,
                                       'message': e.value})
                                )
        else:
            pljson =  {'title': title , 'videos':[] } 
            for song in enjson:
                query_text = song['artist_name']
                query_text += ' ' + song['title']
                for term in terms: query_text += ' ' + term
                if settings.DEBUG: print "searching: "+ query_text + 'type: '+ str(type(query_text))
                vids = youtube.search(query_text)
                if len(vids)>0:
                    pljson['videos'].append({'id': vids[0]['id'], 'title':vids[0]['title']})
            return HttpResponse(dumps({'success':True, 'playlist':pljson}),
                                'application/javascript')
    else:
        return HttpResponse('no data')    
