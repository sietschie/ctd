from weakref import WeakKeyDictionary

class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""
    def __init__(self ):
        self.listeners = WeakKeyDictionary()
        self.eventQueue= []

    #----------------------------------------------------------------------
    def RegisterListener( self, listener ):
        #if not hasattr( listener, "Notify" ): raise blah blah...
        self.listeners[ listener ] = 1

    #----------------------------------------------------------------------
    def UnregisterListener( self, listener ):
        if listener in self.listeners.keys():
            del self.listeners[ listener ]
        
    #----------------------------------------------------------------------
    def Post( self, event ):
        self.eventQueue.append(event)
        
    def Send( self, event ):
        for listener in self.listeners.keys():
            listener.Notify( event )
            
    def SendAll( self ):
        from copy import copy
        events = copy( self.eventQueue )
        self.eventQueue = []
        while len(events) > 0:
            ev = events.pop(0)
            #self.Debug( ev )

            for listener in self.listeners.keys():
                listener.Notify( ev )

        #at the end, notify listeners of the Tick event
        #for listener in self.listeners.keys():
        #    listener.Notify( event )
