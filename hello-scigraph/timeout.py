#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# TIMEOUT CONSTRUCTS
#
# Use like this:
#
# try:
#     with time_limit(MAX_TIMEOUT):
#         # do something...
# except TimeoutException, msg:
#     error = "Timed out!"
#     printDebug(error)
# except Exception, e:
#     error = "Exception: %s" % e
#     printDebug(error)
#
#
# note: the signal package is available only on UNIX systems!
#

import signal
from contextlib import contextmanager

MAX_TIMEOUT = 30 # seconds



class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
