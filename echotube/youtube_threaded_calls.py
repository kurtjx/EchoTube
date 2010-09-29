"""
make some threaded calls to youtube

some trial and error suggests that 3 is an optimal number of threads.
any more risks envoking some kind of gdata throttle that _really_
slows us down - like slower than in serial.

@author kurtjx
@date Tue Sep 28 09:54:18 CDT 2010

"""

import Queue
import threading
import urllib2
import youtube_calls

MAX_THREADS = 3
queue = Queue.Queue()
output = {}

class ThreadTube(threading.Thread):
    '''make threaded calls to Youtube'''
    def __init__(self, queue, output):
        threading.Thread.__init__(self)
        self.queue = queue
	self.output = output

    def run(self):
        while True:
            idx, query = self.queue.get()
            results = youtube_calls.search(query)
	    self.output.update({idx:results})
	    self.queue.task_done()

def search(query_list):
	'''does a threaded call to gdata.youtube for each query in query_list'''
	# empty output
	output = {}
	
	# spawn enough threads
	for query in query_list[:MAX_THREADS]:
		t = ThreadTube(queue, output)
		t.setDaemon(True)
		t.start()
		
	# populate the queue
	for idx, query in enumerate(query_list):
		queue.put((idx, query))

	# wait for threads
	queue.join()

	# sort the output and return
	return [output[key] for key in sorted(output.keys())]
	
	
