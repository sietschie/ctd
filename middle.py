"""This Module glues together the logic and the system modules."""
from xml.dom import minidom
from system import System
from logic import Logic, Level, Wave
from vector import Vector
from eventmanager import EventManager
from events import KeyPressEvent, MouseClickEvent, ClearScreenEvent, QuitEvent, TickEvent
from tickemitter import TickEmitter


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
        self.system.draw_string_at(25, 5, "lives:  %03d" % self.logic.lives )
        self.system.draw_string_at(25, 6, "points: %03d" % self.logic.points )
        self.system.draw_string_at(25, 7, "money:  %03d" % self.logic.money )
        self.system.draw_string_at(25, 8, "num minions:  %03d" % len(self.logic.minions) )

        y = 0
        for minion in self.logic.minions:
            self.system.draw_string_at(25, 9 + y, \
                "minion[" + str(y) + "]:  %s" % str(minion) )
            y += 1

        x = 1
        for w in self.logic.current_level.active_waves:
            self.system.draw_string_at(x, 22, \
                "a: %0.1f, %i" % (w.next_minion_in, w.nr_minion))
            x += 15
        
        w = self.logic.current_level.next_wave
        if w:
            self.system.draw_string_at(x, 22, \
                "n: %0.1f, %0.1f, %i" % (w.offset_wave, w.next_minion_in, w.nr_minion))
            x += 20

        for w in self.logic.current_level.waves:
            self.system.draw_string_at(x, 22, \
                "r: %0.1f, %i" % (w.next_minion_in, w.nr_minion))
            x += 15


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

    def __init__(self):
        self.evm = EventManager()
        
        self.evm.RegisterListener(self)
        
        self.te = TickEmitter(self.evm)
        
        self.system = System(self.evm)
        self.logic = Logic(self.evm)
        
        self.load_map('map.xml')

    def run(self):
        """The main game loop"""
        self.te.Run()



        # restore original settings
        self.system.restorescreen()
