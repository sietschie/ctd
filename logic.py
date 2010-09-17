"""Handles the general game logic"""
import math
from vector import Vector
from events import TickEvent, WaveChangeEvent, QuitEvent

class Level:
    """Contains the description of a level"""
    tiles = {}
    max_x = 0
    max_y = 0
    waypoints = {}
    waves = []
    next_wave = None
    active_waves = []
    
    def __init__(self):
        self.sent_next_wave = False
        
    def send_next_wave(self):
        """Makes the next wave active"""
        if self.next_wave:
            self.active_waves.append(self.next_wave)
            self.sent_next_wave = True
            if self.waves:
                self.next_wave = self.waves[0]
                self.waves.remove(self.next_wave)
            else:
                self.next_wave = None
        
    def update(self, delta):
        """Updates the wave object"""
        if self.next_wave:
            self.next_wave.offset_wave -= delta
            if self.next_wave.offset_wave <= 0:
                self.send_next_wave()
            
        for wave in self.active_waves:
            wave.update(delta)

class Wave:
    """One wave of minions"""
    new_minion = False
    def __init__(self):
        self.next_minion_in = 0
        self.offset_wave = 0
        self.offset_minion = 0
        self.nr_minion = 0
        self.hp_minion = 0
        
    def update(self, delta):
        """updates the status"""
        self.next_minion_in -= delta
        if self.next_minion_in <= 0:
            self.new_minion = True
            self.next_minion_in = self.offset_minion
            
        

class ScreenObject:
    """An Object that appears on screen"""
    def __init__(self, vec):
        self.pos = vec

class MovingObject(ScreenObject):
    """A moving object"""
    def __init__(self, pos, direction = Vector(0, 0)):
        ScreenObject.__init__(self, pos)
        self.dir = direction

class Tower(ScreenObject):
    """A tower shooting bullets"""
    next_shoot_in = 0
    firing_range = 5
    speed = 3
    firepower = 1

    def create_bullet(self, minion):
        """Creates a bullet object heading towards a minion 
        and returns that object.
        """
        bullet =  Bullet(self.pos)
        time = self.vorhalt(minion, bullet)
        bullet.hitpoints = self.firepower

        diff = (minion.pos + minion.dir * time) - bullet.pos
        bullet.dir = diff.set_length(bullet.speed)
        
        return bullet

    def vorhalt(self, minion, bullet):
        """Computes the time when the bullet reaches the minion."""
        a = minion.dir.x**2 + minion.dir.y**2 - \
            bullet.speed**2
        b = 2 * (minion.pos.x - self.pos.x) * minion.dir.x + \
            2 * (minion.pos.y - self.pos.y) * minion.dir.y
        c = math.pow( minion.pos.x - self.pos.x , 2) + \
            math.pow( minion.pos.y - self.pos.y , 2)

        if a == 0: #vllt mit epsilon?
            time = -c / b

        else: # fuer speed ungleich 1, nicht getestet.
            time1 = ( - b + math.sqrt( b * b - 4 * a * c))/(2*a)
            time2 = ( - b - math.sqrt( b * b - 4 * a * c))/(2*a)

            if time1 > 0:
                if time2 > 0:
                    time = min(time1, time2)
                else:
                    time = time1
            else:
                if time2 > 0:
                    time = time2
                #else:
                    # irgendnen fehler?            
        return time


    def find_target(self, minions):
        """Finds the minion closest to tower in firing range."""
        min_dist = 100000
        min_min = 0
        for minion in minions:
            dist = self.pos.Distance(minion.pos)
            
            if dist < min_dist:
                min_dist = dist
                min_min = minion

        if min_dist < self.firing_range:
            return min_min
        else:
            return 0

    def animate(self, delta):
        """Computes time left until next shoot."""
        self.next_shoot_in -= delta

    def shoot(self, minions):
        """Determines target and returns bullet object on success."""
        if self.next_shoot_in < 0: 
            m = self.find_target(minions)

            if m != 0:
                self.next_shoot_in = self.speed
                return self.create_bullet(m)    

class Minion(MovingObject):
    """A normal minion moving down the pathway."""
    speed = 1
    current_wp = 1
    hitpoints = 0
    waypoints = None
    dwp = 5
    wtg = 0
    cwp = Vector(0, 0)

    def __init__(self, waypoints, hitpoints):
        MovingObject.__init__(self, waypoints[0])
        self.waypoints = waypoints
        self.hitpoints = hitpoints
        self.current_wp = 1
        current_waypoint = self.waypoints[self.current_wp]
        self.dir = (current_waypoint - self.pos).set_length(self.speed)

    def __str__(self):
        return "(pos:" + str(self.pos) + \
            ", dir:" + str(self.dir) + \
            ", hp:" + str(self.hitpoints) + ")"
            #", cw:" + str(self.current_wp) + \
            #", dwp:" + str(self.dwp) + \
            #", wtg:" + str(self.wtg) + \
            #", cwp:" + str(self.cwp) + \
            #")"

    def check_if_wp_passed(self, delta):
        current_waypoint = self.waypoints[self.current_wp]
        dist_to_cw = self.pos.Distance(current_waypoint)
        way_to_go = delta*self.speed
        
        self.dwp = dist_to_cw
        self.wtg = way_to_go
        self.cwp = current_waypoint

        while dist_to_cw < way_to_go: # go to next wp
            way_to_go -= dist_to_cw
            self.pos = current_waypoint
            self.current_wp += 1
            if self.current_wp >= len(self.waypoints):
                return 0.0

            current_waypoint = self.waypoints[self.current_wp]
            dist_to_cw = self.pos.Distance(current_waypoint)
            self.dir = (current_waypoint - self.pos).set_length(self.speed)

        return way_to_go / self.speed

    def animate(self, delta):
        """Computes new position."""
        delta_res = self.check_if_wp_passed(delta)
        self.pos += self.dir * delta_res

class Bullet(MovingObject):
    """A bullet flying down a straight line."""
    speed = 1.5
    hitpoints = 1

    def animate(self, delta):
        """Computes new position."""
        self.pos += self.dir * delta


class Logic:
    """Holds the game logic."""
    minions = []
    bullets = []
    towers = []
    current_level = None
    money = None
    points = None
    lives = None

    def __init__(self, evm):
        self.evm = evm
        evm.RegisterListener(self)

        self.money = 10
        self.points = 0
        self.lives = 5


    def add_tower(self, x, y):
        """Checks for boundaries and adds tower on success."""
        if self.money < 5:
            return

        self.money -= 5
        
        if x >= 1 :
            if x <= self.current_level.max_x : 
                if y >= 1 :
                    if y <= self.current_level.max_y:
                        if self.current_level.tiles[x, y] == 0:
                            for tower in self.towers:
                                if tower.pos.x == x: 
                                    if tower.pos.y == y:
                                        return
                            tower = Tower(Vector(x, y))
                            self.towers.append(tower)

    def add_minion(self, hitpoints=1):
        """Adds minion on beginning of the pathway."""
        self.minions.append(Minion(self.current_level.waypoints, hitpoints))

    def check_for_finished_minions(self):
        """Check if minion reached end of pathway."""
        for minion in self.minions[:]:
            if minion.current_wp == len(minion.waypoints):
                self.lives -= 1
                self.minions.remove(minion)

    def collision_detection(self):
        """Checks if bullet reached a minion. If yes, both are deleted."""
        for bullet in self.bullets[:]:
            if int(bullet.pos.x) < 1:
                self.bullets.remove(bullet)
                continue
            if int(bullet.pos.x) > self.current_level.max_x:
                self.bullets.remove(bullet)
                continue
            if int(bullet.pos.y) < 1:
                self.bullets.remove(bullet)
                continue
            if int(bullet.pos.y) > self.current_level.max_y:
                self.bullets.remove(bullet)
                continue

        for bullet in self.bullets[:]:
            for minion in self.minions:
                if minion.hitpoints > 0:
                    #TODO: pos1 == pos2
                    if int(bullet.pos.x) == int(minion.pos.x):
                        if int(bullet.pos.y) == int(minion.pos.y):
                            minion.hitpoints -= bullet.hitpoints
                            self.bullets.remove(bullet)
                            break

        for minion in self.minions[:]:
            if minion.hitpoints <= 0:
                self.minions.remove(minion)
                self.points += 1
                self.money += 1
                
    def Notify(self, event):
        if isinstance( event, TickEvent ):
            self.animate(event.delta)

    def animate(self, delta):
        """Computes new state of the game."""
        for minion in self.minions[:]:
            minion.animate(delta)
            #if minion.reached_end:
                #self.minions.remove(minion)
                #self.lives -= 1
        for tower in self.towers:
            tower.animate(delta)
        for bullet in self.bullets:
            bullet.animate(delta)
        self.check_for_finished_minions()
        self.collision_detection()
        for tower in self.towers:
            bullet = tower.shoot(self.minions)
            if bullet != None:
                self.bullets.append(bullet)
        
        self.current_level.update(delta)
        
        if self.current_level.sent_next_wave:
            self.current_level.sent_next_wave = False
            self.evm.Post(WaveChangeEvent())
        
        for wave in self.current_level.active_waves[:]:
            if wave.new_minion:
                wave.new_minion = False
                wave.nr_minion -= 1
                self.add_minion(wave.hp_minion)
                self.evm.Post(WaveChangeEvent())
                if wave.nr_minion == 0:
                    self.current_level.active_waves.remove(wave)
        
        if self.lives <= 0:
            self.evm.Post(QuitEvent())
                    
        if not self.minions and not self.current_level.active_waves and not self.current_level.next_wave:
            self.evm.Post(QuitEvent())
