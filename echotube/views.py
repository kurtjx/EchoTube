from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from EchoTube.echotube.models import Playlist, Video
from simplejson import dumps
from datetime import datetime
from hashlib import md5

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
        ip = request.META['REMOTE_ADDR']

        # check if we've seen these exact GET params
        rhash = md5(str(request.GET)).hexdigest()
        try:
            pl = Playlist.objects.get(request__exact=rhash)
            pljson = make_playlist_json(pl)
            if settings.DEBUG: print "returning playlist from DB"
            return HttpResponse(dumps({'success':True, 'playlist':pljson}), 'application/javascript')
        except Playlist.DoesNotExist:
            pass
            
        
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
        if settings.DEBUG: start = time.time()
        try:
            enjson = echonest.playlist_description(descriptions, artists, params)
            if settings.DEBUG:
                print "echonest call time: %s" % (time.time()-start)
            if len(enjson)==0:
                raise echonest.EchonestAPIException('zero songs found')
        except echonest.EchonestAPIException, e:
            return HttpResponse(dumps({'success':False,
                                       'message': e.value})
                                )
        else:
            playlist = Playlist(title = title,
                                date = datetime.now(),
                                ip = ip,
                                request = rhash
                                )
            playlist.save()
            pljson =  {'title': title , 'videos':[] , 'uri':'/playlist/'+str(playlist.pk)}
            query_list = []
            if settings.DEBUG: start = time.time()
            idx = 0
            for song in enjson:
                query_text = song['artist_name']
                query_text += ' ' + song['title']
                for term in terms: query_text += ' ' + term
                if THREADED:
                    query_list.append(query_text)
                else:
                    feed = youtube.search(query_text)
                    if len(feed)>0:
                        pljson['videos'].append({'id': feed[0]['id'],
                                                 'title':feed[0]['title']})
                        video = Video(playlist = playlist,
                                      youtube_id = feed[0]['id'],
                                      title = feed[0]['title'],
                                      idx = idx)
                        video.save()
                        idx+=1
            # threaded youtube calls to get feeds
            if THREADED:
                feeds = youtube.search(query_list)
                for feed in feeds:
                    if len(feed)>0:
                        pljson['videos'].append({'id': feed[0]['id'],
                                                 'title':feed[0]['title']})
                        video = Video(playlist = playlist,
                                      youtube_id = feed[0]['id'],
                                      title = feed[0]['title'],
                                      idx = idx)
                        video.save()
                        idx+=1
            if len(pljson['videos'])==0:
                playlist.delete()
                return HttpResponse(dumps({'success':False, 'message':'search failed'}),
                                'application/javascript')
            if settings.DEBUG: print "elapsed time for youtube: %s" % (time.time() - start)
            return HttpResponse(dumps({'success':True, 'playlist':pljson}),
                                'application/javascript')
    else:
        return HttpResponse('no data')    

def playlist(request, pk):
    # django shortcut to get playlist from db
    pl = get_object_or_404(Playlist, pk=pk)
    pljson = make_playlist_json(pl)
    return render_to_response('playlist.html',{'playlist':dumps(pljson),
                                               'debug': settings.DEBUG,
                                               'title': pl.title})
    
def make_playlist_json(pl):
    vids = Video.objects.filter(playlist=pl).order_by('idx')
    pljson = {'title': pl.title, 'videos':[], 'uri': '/playlist/'+str(pl.pk)}
    for vid in vids:
        pljson['videos'].append({'id': vid.youtube_id,
                         'title':vid.title,
                         })
    return pljson
    
