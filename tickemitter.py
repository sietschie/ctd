import time
from events import TickEvent, QuitEvent

class TickEmitter:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        self.keepGoing = 1
        
        self.current_time = 0
        self.last_time = 0
        self.delta = 0

    def update_time(self):
        """computes difference between last and current time, 
        result in delta
        """
        self.last_time = self.current_time
        self.current_time = time.time()
        self.delta = self.current_time - self.last_time
        #self.delta = 1/60
        
    #----------------------------------------------------------------------
    def Run(self):
        while self.keepGoing:
            self.update_time()
            event = TickEvent(self.delta)
            self.evManager.Post( event )

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, QuitEvent ):
            #this will stop the while loop from running
            self.keepGoing = False
