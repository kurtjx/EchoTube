from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from simplejson import dumps

THREADED = True

import echonest_calls as echonest
if THREADED:
    import youtube_threaded_calls as youtube
else:
    import youtube_calls as youtube

if settings.DEBUG: import time


def api(request):
    if request.GET:
        descriptions = request.GET.getlist('description')
        artists = request.GET.getlist('artist')
        terms = request.GET.getlist('term')
        
        if len(descriptions)>0 and descriptions[0]!='':
            title = descriptions[0]
        elif len(artists)>0:
            title = artists[0]
            if descriptions[0]=='': descriptions=[]
        else:
            title = 'untitled'
        if settings.DEBUG: print 'title is: '+title
        params = {}
        for key,value in request.GET.items():
            if key != 'description' and key != 'artist' and key!='term' and value !='':
                params.update({key:value})
        start = time.time()
        try:
            enjson = echonest.playlist_description(descriptions, artists, params)
            if settings.DEBUG: print "echonest call time: %s" % (time.time()-start)
            if len(enjson)==0: raise echonest.EchonestAPIException('zero songs found')
        except echonest.EchonestAPIException, e:
            return HttpResponse(dumps({'success':False,
                                       'message': e.value})
                                )
        else:
            pljson =  {'title': title , 'videos':[] }
            query_list = []
            start = time.time()
            for song in enjson:
                query_text = song['artist_name']
                query_text += ' ' + song['title']
                for term in terms: query_text += ' ' + term
                if settings.DEBUG: print "searching: "+ query_text + ' type: '+ str(type(query_text))
                if THREADED: query_list.append(query_text)
                else:
                    feed = youtube.search(query_text)
                    if len(feed)>0:
                        pljson['videos'].append({'id': feed[0]['id'],
                                                 'title':feed[0]['title']})
            # threaded youtube calls to get feeds
            if THREADED:
                feeds = youtube.search(query_list)
                for feed in feeds:
                    if len(feed)>0:
                        pljson['videos'].append({'id': feed[0]['id'],
                                                 'title':feed[0]['title']})
            if settings.DEBUG: print "elapsed time for youtube: %s" % (time.time() - start)
            return HttpResponse(dumps({'success':True, 'playlist':pljson}),
                                'application/javascript')
    else:
        return HttpResponse('no data')    
