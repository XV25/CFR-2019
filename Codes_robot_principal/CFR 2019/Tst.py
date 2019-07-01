# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:02:30 2019

@author: ehnla
"""



#
#def stop():
#    print("Stop_robot")
#    sys.exit(1)
#
#
#t = threading.Timer(10,stop)
#t.start()
##n_ori = threading.active_count()
##print(n_ori)
#for i in range(100):
#    print(i)
#    time.sleep(0.5)
#    #n = threading.active_count()
#    #print(n)
#    #print(t.isAlive())
#    if t.isAlive() == 0 :
#        sys.exit(1)
#
#
#def run():
#    while True:
#        #mettre programme robot
#        
#    
#import threading
#import time

import time
import threading
import signal
 
class Job(threading.Thread):
 
    def __init__(self):
        threading.Thread.__init__(self)
 
        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        
        self.shutdown_flag = threading.Event()
        #self.tm = threading.Timer(10,stop)
 
        # ... Other thread setup code here ...
 
    def run(self):
        print('Thread #%s started' % self.ident)
 
        while not self.shutdown_flag.is_set():
            # ... Job code here ...
            time.sleep(0.5)
 
        # ... Clean shutdown code here ...
        print('Thread #%s stopped' % self.ident)
 
#    def stop(self):
#        print("End_robot")
#        self.tm = False
#        return(False)
 
class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass
 
 
def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

    
    
def main():
 
    # Register the signal handlers
 #   signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    signal.signal(signal.SIGALRM, service_shutdown)
    signal.alarm(5)

    print('Starting main program')
 
    # Start the job threads
    try:
        j1 = Job()
        j2 = Job()
        j1.start()
        j2.start()
 
        # Keep the main thread running, otherwise signals are ignored.
        while True:
            time.sleep(0.5)
            print("Ok")

    
    
    except ServiceExit:
        # Terminate the running threads.
        # Set the shutdown flag on each thread to trigger a clean shutdown of each thread.
        j1.shutdown_flag.set()
        j2.shutdown_flag.set()
        # Wait for the threads to close...
        j1.join()
        j2.join()
    

 
    print('Exiting main program')
 
 
if __name__ == '__main__':
    main()