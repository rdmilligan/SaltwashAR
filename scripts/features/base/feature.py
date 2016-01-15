# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from threading import Thread

class Feature:
  
    # initialize feature
    def __init__(self):
        self.thread = None
        self.is_stop = False

    # start thread
    def start(self, args=None):
        self.is_stop = False
        
        if self.thread and self.thread.is_alive(): return

        self.thread = Thread(target=self._thread, args=(args,))
        self.thread.start()

    # stop thread
    def stop(self):
        self.is_stop = True