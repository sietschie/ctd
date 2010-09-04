"""This Module glues together the logic and the system modules."""
import time
from xml.dom import minidom
from system import System
from logic import Logic, Level, Wave


# global variables
class Middle:
    """It handles the input, keeps track of time and draws objects to
    the screen.
    """

    current_time = 0
    last_time = 0
    delta = current_time - last_time

    system = System()
    logic = Logic()
    def restore(self):
        """things to before shutdown"""
        System.restorescreen()

    def update_time(self):
        """computes difference between last and current time, 
        result in delta
        """
        self.last_time = self.current_time
        self.current_time = time.time()
        self.delta = self.current_time - self.last_time
            
    def draw_minions(self):
        """Draws minions to screen."""
        for minion in self.logic.minions:
            self.system.draw_at(int(minion.x), int(minion.y), 'o', 
                self.system.COLOR_BLACK, self.system.COLOR_YELLOW)

    def draw_bullets(self):
        """Draws bullets to screen."""
        for bullet in self.logic.bullets:
            if self.logic.current_level.tiles[int(bullet.x), int(bullet.y)] == 0:
                self.system.draw_at(int(bullet.x), int(bullet.y), '*', 
                    self.system.COLOR_BLACK, self.system.COLOR_GREEN)
            else:
                self.system.draw_at(int(bullet.x), int(bullet.y), '*', 
                    self.system.COLOR_BLACK, self.system.COLOR_YELLOW)

    def draw_towers(self):
        """Draws towers to screen."""
        for tower in self.logic.towers:
            self.system.draw_at(int(tower.x), int(tower.y), '#', 
                self.system.COLOR_BLACK, self.system.COLOR_GREEN)

    def draw_map(self):
        """Draws map to screen."""
        for x in range(1, 21):
            for y in range(1, 21):
                if self.logic.current_level.tiles[x, y] == 0:
                    self.system.draw_at(x, y, ' ', 
                        self.system.COLOR_GREEN, self.system.COLOR_GREEN)
                else:
                    self.system.draw_at(x, y, ' ', 
                        self.system.COLOR_YELLOW, self.system.COLOR_YELLOW)
                        
    def draw_hud(self):
        """draws hud to screen"""
        self.system.draw_string_at(25, 5, "lives:  %03d" % self.logic.lives )
        self.system.draw_string_at(25, 6, "points: %03d" % self.logic.points )
        self.system.draw_string_at(25, 7, "money:  %03d" % self.logic.money )
        self.system.draw_string_at(25, 8, "num minions:  %03d" % len(self.logic.minions) )

        if self.logic.minions:
            self.system.draw_string_at(25, 9, \
                "minion[0].x:  %f" % (self.logic.minions[0].x) )
            self.system.draw_string_at(25, 10, \
                "minion[0].y:  %f" % (self.logic.minions[0].y) )

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


        level = Level()
        level.max_y = int(map_tag.getElementsByTagName('rows')[0].firstChild.data)
        level.max_x = int(map_tag.getElementsByTagName('columns')[0].firstChild.data)

        row_tag = map_xml.getElementsByTagName('row')

        for row in row_tag:
            row_data = row.firstChild.data
            y = int(row.attributes['pos'].value)
            for x in range(1, len(row_data)+1):
                level.tiles[x, y] = int(row_data[x-1])

        wps_tag = map_xml.getElementsByTagName('waypoints')
        wp_tag = wps_tag[0].getElementsByTagName('waypoint')

        for waypoint in wp_tag:    
            number = int( waypoint.attributes['nr'].value )
            x = int( waypoint.getElementsByTagName('x')[0].firstChild.data )
            y = int( waypoint.getElementsByTagName('y')[0].firstChild.data )

            level.waypoints[number] = [x, y]

        wvs_tag = map_xml.getElementsByTagName('waves')
        wv_tag = wvs_tag[0].getElementsByTagName('wave')

        for wave in wv_tag:    
            offset_wave = int( wave.getElementsByTagName('offset_wave')[0].firstChild.data )
            offset_minion = int( wave.getElementsByTagName('offset_minion')[0].firstChild.data )
            nr_minion = int( wave.getElementsByTagName('nr_minion')[0].firstChild.data )
            hp_minion = int( wave.getElementsByTagName('hp_minion')[0].firstChild.data )

            level.waypoints[number] = [x, y]

            w = Wave()
            w.offset_wave = offset_wave
            w.offset_minion = offset_minion
            w.hp_minion = hp_minion
            w.nr_minion = nr_minion

            level.waves.append(w)
            
        level.next_wave = level.waves[0]
        level.waves.remove(level.next_wave)        

        self.logic.current_level = level

    def __init__(self):
        self.load_map('map.xml')

        self.last_time = time.time()
        self.current_time =  time.time()


    def run(self):
        """The main game loop"""
        while True:
            # read character from keyboard
            char = self.system.getch()
            # was returned as an integer (ASCII); make it a character
            if char != -1:
                if char == self.system.KEY_MOUSE:
                    #device_id, x, y, z, button = self.system.getmouse()
                    ret = self.system.getmouse()
                    x = ret[1]
                    y = ret[2]
                    self.logic.add_tower(x, y)
                else:
                    char = chr(char)
                    # quit?
                    if char == 'q': 
                        break
                    if char == 'a':
                        self.logic.add_minion()
                    if char == ' ':
                        self.logic.current_level.send_next_wave()
            self.update_time()
            self.logic.animate(self.delta)
            self.system.scrn.erase()
            self.draw_map()
            self.draw_minions()
            self.draw_towers()
            self.draw_bullets()
            self.draw_hud()
            time.sleep(0.01)

        # restore original settings
        self.system.restorescreen()
