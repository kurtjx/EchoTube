'''
Created on May 14, 2010

@author: kurtjx
'''

from urllib import quote
import gdata.youtube.service
import unicodedata

def search(query_text):
    print type(query_text)
    # TODO fucking fix fucking unicode shit
    name = query_text.encode('ascii','replace')
    service = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    query.categories.append("Music")
    query.racy = "exclude"
    query.vq = name
    feed = service.YouTubeQuery(query)
    results = []
    for video in feed.entry:
        result = {'title': video.title.text,
                  'url': video.media.player.url,
                  'id': video.id.text.split('/')[-1]}
        results.append(result)
    return results
