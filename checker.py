from urlparse import urlparse
from threading import Thread
import httplib, sys
from Queue import Queue

concurrent = 10

def doWork():
    while True:
        url=q.get()
        status,url=getStatus(url)
        doSomethingWithResult(status,url)
        q.task_done()

def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = httplib.HTTPConnection(url.netloc)   
        conn.request("GET", url.path)
        res = conn.getresponse()
        server = res.getheader('server')
        data = res.read()
        print res.status, server, ourl
        index = data.find("href")
        if (index > 0):
            print "yahooo, got one: " + ourl
            w = open("found", "w")
            w.write(ourl)
            w.close()
            
        return res.status, ourl
    except:
        return "error", ourl

def doSomethingWithResult(status, url):
    print status, url

q=Queue(concurrent*2)
for i in range(concurrent):
    t=Thread(target=doWork)
    t.daemon=True
    t.start()
try:
    for line in open('top-1m.csv'):
        f = line.split(',')[-1]
        url = "http://" + f[:-1] + "/req"
        q.put(url.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)