import Queue
import threading
import urllib2
import youtube_calls

queue = Queue.Queue()
output = {}

class ThreadTube(threading.Thread):
    '''make threaded calls to Youtube'''
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            idx, query = self.queue.get()
            results = youtube_calls.search(query)
			output.update({idx:results})

def search(query_list):
	'''does a threaded call to gdata.youtube for each query in query_list'''
	# empty output
	output = {}
	threads = ThreadTube(queue)
	# populate the queue
	for idx, query in query_list:
		queue.put((idx, query))
	# run it
	threads.run()
	return [result for result in output.values()]
	
	
