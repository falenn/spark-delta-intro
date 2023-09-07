#!/usr/bin/env python

from time import time
from datetime import timedelta

class T():
    def __enter__(self):
        self.start = time()
    def __exit__(self, type, value, traceback):
        self.end = time()
        elapsed = self.end - self.start
        print(str(timedelta(seconds=elapsed)))
