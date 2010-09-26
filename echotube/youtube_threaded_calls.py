import Queue
import threading
import urllib2
import youtube_calls

queue = Queue.Queue()

class ThreadTube(threading.Thread):
    '''make threaded calls to Youtube'''
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            query = self.queue.get()

            results = youtube_calls.search(query)
