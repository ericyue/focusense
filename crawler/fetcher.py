import urllib2
import time
from gzip_deflate_support import *
from Queue import Queue
from threading import Thread,Lock
from threading import stack_size
import socket

socket.setdefaulttimeout(120)
stack_size(32768*16)

class Fetcher:
    def __init__(self,threads):
        encoding_support = ContentEncodingProcessor
        self.opener = urllib2.build_opener(encoding_support,urllib2.HTTPHandler)
        self.lock = Lock()
        self.urls = Queue()
        self.output = Queue()
        self.threads = threads
        for i in range(threads):
            t = Thread(target=self.process,args=(i,))
            t.setName=i
            print 'THREAD %3d RUN        '.rjust(150) % i
            t.setDaemon(True)
            t.start()
        self.running = 0
 
    def __del__(self):
        self.urls.join()
        self.output.join()
 
    def taskleft(self):
        return self.urls.qsize()+self.output.qsize()+self.running
 
    def push(self,req):
        self.urls.put(req)
 
    def pop(self):
        return self.output.get()
        
    def get(self,req,retries=3):
        try:
            response = self.opener.open(req)
            data = response.read()
        except Exception , what:
            print what,req
            if retries>0:
                return self.get(req,retries-1)
            else:
                print 'GET Failed',req
                return ''
        return data
                
    def process(self,i):
        while True:
            req = self.urls.get()
            with self.lock:
                self.running += 1

            content = self.get(req) 
            # self.opener.open(req).read()
            print 'THREAD %3d GOT THE CONTENT'.rjust(150) %i
            self.output.put((req,content))
            with self.lock:
                self.running -= 1
            self.urls.task_done()
            time.sleep(0.1)