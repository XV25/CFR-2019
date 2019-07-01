# -*- coding: utf-8 -*-
"""
Created on Thu May 30 08:05:12 2019

@author: ehnla
"""

import sys
import signal
import time

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    sys.exit(1)

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, service_shutdown)
    signal.alarm(5)
    i = 0
    while True : 
        i += 1
        print(i)
        time.sleep(0.5)
    