import threading
import Queue
import time
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError

# The worker thread gets jobs off the queue.  When the queue is empty, it
# assumes there will be no more work and exits.
# (Realistically workers will run until terminated.)
def worker ():
    print 'Running worker'
    time.sleep(0.1)
    while True:
        try:
            arg = q.get(block=False)
        except Queue.Empty:
            print 'Worker', threading.currentThread(),
            print 'queue empty'
            break
        else:
            print 'Worker', threading.currentThread(),
            print 'running with argument', arg
            url = urllib2.Request(arg)
            try:
                response = urlopen(url, timeout=3)
            except:
                print 'We failed to reach a server.'
            else:
                try:
                    text = response.read()
                    index = text.find("href")
                    if (index > 0):
                        print "yahooo, got one: " + arg
                        w = open("found", "a")
                        w.write(arg)
                        w.close()
                except:
                    print "can't read from response"
                        
# Create queue
q = Queue.Queue()

# Start a pool of 5 workers
for i in range(5):
    t = threading.Thread(target=worker, name='worker %i' % (i+1))
    t.start()

# Begin adding work to the queue
for line in open('urls'):
    f = line.split(',')[-1]
    host = "http://" + f[:-1] + "/request"
    q.put(host)
    
# Give threads time to run
print 'Main thread sleeping'
time.sleep(5)