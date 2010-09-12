from events import InputEvent
from events import TickEvent, QuitEvent
import pickle

class InputRecorder:
    """..."""
    def __init__(self, evManager, filename):
        self.evManager = evManager
        self.evManager.RegisterListener( self )
        self.event_list = []
        self.filename = filename
        
    def Notify(self, event):
        if isinstance( event, InputEvent ):
            self.event_list.append(event)
        elif isinstance( event, TickEvent ):
            self.event_list.append(event)
        elif isinstance( event, QuitEvent ):
            with open(self.filename, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(self.event_list, f, -1)        

class InputPlayer:
    def __init__(self, evManager, filename):
        self.evManager = evManager
        self.evManager.RegisterListener( self )
        self.event_list = []
        with open(filename, 'rb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            self.event_list = pickle.load(f)    
            
    def Run(self):
        for event in self.event_list:
            self.evManager.Post( event )

    def Notify(self, event):
        pass
