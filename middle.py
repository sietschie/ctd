"""This Module glues together the logic and the system modules."""

from xml.dom import minidom
from system import System
from logic import Logic, Level, Wave
from vector import Vector
from eventmanager import EventManager
from events import KeyPressEvent, MouseClickEvent, ClearScreenEvent, QuitEvent, TickEvent, WaveChangeEvent
from tickemitter import TickEmitter
from inputrecorder import InputRecorder, InputPlayer

class Widget:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height      
        self.border = True
        self.border_bold = False
        self.show = True
        self.invert = False  
        self.label = ''
        self.children = []
        self.offset = (0,0)
        self.border = True
        
    def add_child(self, child):
        self.children.append(child)
        child.set_offset((self.x, self.y))
        
    def set_offset(self, offset):
        self.offset = offset
        child_offset = (offset[0] + self.x, offset[1] + self.y )
        for w in self.children:
            w.set_offset(child_offset)
            
class WaveWidget(Widget):
    def __init__(self, x, y, width, height):
        Widget.__init__(self, x, y, width, height)
        self.time = Widget(1,1,width-2, 1)
        self.nr_minions = Widget(1,2,width-2, 1)
        self.add_child(self.time)
        self.add_child(self.nr_minions)
        self.time.border = False
        self.nr_minions.border = False
        
    def show_time(self, show):
        self.time.show = show
        
    def set_time(self, time):
        self.time.label = "time left: %0.1f" % time

    def set_nr(self, nr):
        self.nr_minions.label = "nr of minions: %i" % nr


class WidgetController:
    def __init__(self, evm, system):
        self.evm = evm
        evm.RegisterListener(self)
        
        self.system = system
        (max_x, max_y) = system.scrn.getmaxyx()

    def Notify(self, event):
        pass

    def draw_widgets(self, widget):
        stack = [widget]
        
        while stack:
            w = stack.pop()
            if w.show:
                stack.extend(w.children)
                self.draw_widget(w)
        #current_position = (0,0)
        
        
    def draw_widget(self, widget):
        if widget.border:
            self.draw_border(widget)
        self.draw_label(widget)
        
    def draw_label(self, widget):   
        width = widget.width
        height = widget.height
        x = widget.x + widget.offset[0]
        y = widget.y + widget.offset[1]
        label = widget.label
        size = len(label)
        
        pos_x = int(x + (width+1)/2 - (size + 1)/2)
        pos_y = int(y + height/2)
        
        self.system.draw_string_at(pos_x, pos_y, label)
        
    def draw_border(self, widget):   
        width = widget.width
        height = widget.height
        x = widget.x + widget.offset[0]
        y = widget.y + widget.offset[1]
        
        if widget.border_bold:
            border_line = '┏'+((width - 2)*'━')+'┓'
            self.system.draw_string_at(x, y, border_line)
            border_line = '┗'+((width - 2)*'━')+'┛'
            self.system.draw_string_at(x, y + height - 1, border_line)
            for i in range(1, height-1):
                self.system.draw_string_at(x, y + i, '┃')
                self.system.draw_string_at(width + x - 1, y + i, '┃')
        else:
            border_line = '┌'+((width - 2)*'─')+'┐'
            self.system.draw_string_at(x, y, border_line)
            border_line = '└'+((width - 2)*'─')+'┘'
            self.system.draw_string_at(x, y + height - 1, border_line)
            for i in range(1, height-1):
                self.system.draw_string_at(x, y + i, '│')
                self.system.draw_string_at(width + x - 1, y + i, '│')
        
# global variables
class Middle:
    """It handles the input, keeps track of time and draws objects to
    the screen.
    """

    @staticmethod
    def restore():
        """things to before shutdown"""
        System.restorescreen()


            
    def draw_minions(self):
        """Draws minions to screen."""
        for minion in self.logic.minions:
            self.system.draw_at(minion.pos.to_int(), 'o', 
                self.system.COLOR_BLACK, self.system.COLOR_YELLOW)

    def draw_bullets(self):
        """Draws bullets to screen."""
        for bullet in self.logic.bullets:
            if self.logic.current_level.tiles[int(bullet.pos.x), int(bullet.pos.y)] == 0:
                self.system.draw_at(bullet.pos.to_int(), '*', 
                    self.system.COLOR_BLACK, self.system.COLOR_GREEN)
            else:
                self.system.draw_at(bullet.pos.to_int(), '*', 
                    self.system.COLOR_BLACK, self.system.COLOR_YELLOW)

    def draw_towers(self):
        """Draws towers to screen."""
        for tower in self.logic.towers:
            self.system.draw_at(tower.pos.to_int(), '#', 
                self.system.COLOR_BLACK, self.system.COLOR_GREEN)

    def draw_map(self):
        """Draws map to screen."""
        for x in range(1, 21):
            for y in range(1, 21):
                if self.logic.current_level.tiles[x, y] == 0:
                    self.system.draw_at(Vector(x, y), ' ', 
                        self.system.COLOR_GREEN, self.system.COLOR_GREEN)
                else:
                    self.system.draw_at(Vector(x, y), ' ', 
                        self.system.COLOR_YELLOW, self.system.COLOR_YELLOW)
                        
    def draw_hud(self):
        """draws hud to screen"""
        self.windows['lives'].label = "lives:  %03d" % self.logic.lives
        self.windows['points'].label = "points: %03d" % self.logic.points
        self.windows['money'].label = "money:  %03d" % self.logic.money

    def load_map(self, file_name):
        """Loads map from xml file"""
        map_xml = minidom.parse(file_name)

        map_tag = map_xml.getElementsByTagName('map')[0]

        def get_data(elem, tag):
            return elem.getElementsByTagName(tag)[0].firstChild.data

        level = Level()
        level.max_y = int(get_data(map_tag, 'rows'))
        level.max_x = int(get_data(map_tag,'columns'))

        row_tag = map_xml.getElementsByTagName('row')

        for row in row_tag:
            row_data = row.firstChild.data
            y = int(row.attributes['pos'].value)
            for x in range(1, len(row_data)+1):
                level.tiles[x, y] = int(row_data[x-1])

        for waypoint in map_xml.getElementsByTagName('waypoint'):    
            number = int( waypoint.attributes['nr'].value )
            x = int( get_data(waypoint,'x'))
            y = int( get_data(waypoint,'y'))

            level.waypoints[number] = Vector(x, y)

        for wave in map_xml.getElementsByTagName('wave'):    
            w = Wave()
            w.offset_wave = int( get_data(wave, 'offset_wave'))
            w.offset_minion = int( get_data(wave, 'offset_minion'))
            w.hp_minion = int( get_data(wave, 'hp_minion'))
            w.nr_minion = int( get_data(wave, 'nr_minion'))

            level.waves.append(w)
            
        level.next_wave = level.waves[0]
        level.waves.remove(level.next_wave)        

        self.logic.current_level = level

    def Notify(self, event):
        if isinstance( event, KeyPressEvent ):
            if event.key == 'q': 
                self.evm.Post(QuitEvent())
            if event.key == 'a':
                self.logic.add_minion()
            if event.key == ' ':
                self.logic.current_level.send_next_wave()
                
        elif isinstance( event, MouseClickEvent ):
            self.logic.add_tower(event.pos.x, event.pos.y)
        elif isinstance( event, TickEvent ):
            self.evm.Send(ClearScreenEvent())
            self.draw_map()
            self.draw_minions()
            self.draw_towers()
            self.draw_bullets()
            self.draw_hud()
            
            self.wc.draw_widgets(self.main_window)

            if self.logic.current_level.next_wave and len(self.logic.current_level.active_waves) < len(self.wave_windows):
                self.wave_windows[len(self.logic.current_level.active_waves)].set_time(self.logic.current_level.next_wave.offset_wave)


        elif isinstance( event, WaveChangeEvent ):
            wavelist = []
            wavelist.extend(self.logic.current_level.active_waves)
            if self.logic.current_level.next_wave:
                wavelist.append(self.logic.current_level.next_wave)
            wavelist.extend(self.logic.current_level.waves)
            
            for i in range(0, min(len(self.wave_windows), len(wavelist))):
                wave = wavelist[i]
                window = self.wave_windows[i]
                window.set_nr(wave.nr_minion)
                window.border_bold = False
                window.show_time(False)

            for i in range(min(len(self.wave_windows), len(wavelist)),len(self.wave_windows)):
                self.wave_windows[i].show = False
                
            if self.logic.current_level.next_wave and len(self.logic.current_level.active_waves) < len(self.wave_windows):
                self.wave_windows[len(self.logic.current_level.active_waves)].border_bold = True
                self.wave_windows[len(self.logic.current_level.active_waves)].show_time(True)

    def __init__(self):

        from optparse import OptionParser
        parser = OptionParser(version="%prog 0.1.1")
        parser.add_option('-r', '--replay', 
                            dest='infile',
                            help='uses the recorded input instead of the user input')
        parser.add_option('-d', '--dump', 
                            dest='outfile',
                            help='writes the user input into a file')
        (options, args) = parser.parse_args()
        
        self.evm = EventManager()
        
        self.evm.RegisterListener(self)

        if options.infile:
            self.te = InputPlayer(self.evm, options.infile)
        else:
            self.te = TickEmitter(self.evm)
        
        self.system = System(self.evm)
        self.logic = Logic(self.evm)
        
        if options.outfile:
            self.input_recorder = InputRecorder(self.evm, options.outfile)
        
        self.load_map('map.xml')
        
        #########################################
        ## create windows
        #########################################
        
        self.main_window = Widget(0,0,110,27)
        self.window = Widget(84,1,25,25)

        self.windows = {}

        self.windows['lives'] = Widget(1,1,23,3)
        self.windows['money'] = Widget(1,4,23,3)
        self.windows['points'] = Widget(1,7,23,3)

        for w in self.windows.values():
            self.window.add_child(w)
            
        self.main_window.add_child(self.window)

        self.wave_window = Widget(58,1,25,25)
        self.main_window.add_child(self.wave_window)
        
        wave_label = Widget(1,1,23,1)
        wave_label.label = 'Waves'
        wave_label.border = False
        self.wave_window.add_child(wave_label)

        self.wave_windows = []
        for i in range(0,4):
            w = WaveWidget(1,2 + i * 5, 23, 5)
            self.wave_windows.append(w)
            self.wave_window.add_child(w)
            
        self.wc = WidgetController(self.evm,self.system)
        
        help_window = Widget(1,22,56,4)

        help_window1 = Widget(0,1,56,1)
        help_window1.label = "Press space to send next wave. Hit q to quit the game."
        help_window1.border = False
        help_window.add_child(help_window1)

        help_window2 = Widget(0,2,56,1)
        help_window2.label = "Click anywhere on the map to place a tower."
        help_window2.border = False
        help_window.add_child(help_window2)
        
        self.main_window.add_child(help_window)

    def run(self):
        """The main game loop"""
        self.te.Run()

        # restore original settings
        self.system.restorescreen()
