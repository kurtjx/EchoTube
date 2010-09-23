import urllib
import simplejson

# kurtjx's api key hard coded, nice
ECHO_NEST_API_KEY = 'NN5CXYTRMEXRFSPZZ'

def playlist_description(descriptions=[], artists=[], params=None):
    params.update({'api_key':ECHO_NEST_API_KEY,
              'format':'json',
              'type':'artist-radio',
             })
    for k,v in params.items():
        if isinstance(v, unicode):
            params[k] = v.encode('utf-8')
    params = urllib.urlencode(params)
    url = 'http://developer.echonest.com/api/v4/playlist/static?%s' % params
    for description in descriptions:
        url+='&description='+urllib.quote_plus(description.encode('utf-8'))
    for artist in artists:
        url+='&artist='+urllib.quote_plus(artist.encode('utf-8'))
    print url
    f = urllib.urlopen(url)
    response = simplejson.loads(f.read())['response']
    print response
    if response['status']['code'] == 0:
        return response['songs']
    else:
        print response
        return None
