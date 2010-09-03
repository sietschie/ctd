"""Handles the general game logic"""
import math

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
		pass
		
	def send_next_wave(self):
		if self.next_wave:
			self.active_waves.append(self.next_wave)
			if self.waves:
				self.next_wave = self.waves[0]
				self.waves.remove(self.next_wave)
			else:
				self.next_wave = None
		
	def update(self, delta):
		if self.next_wave:
			self.next_wave.offset_wave -= delta
			if self.next_wave.offset_wave <= 0:
				self.send_next_wave()
			
		for w in self.active_waves:
			w.update(delta)

class Wave:
	new_minion = False
	def __init__(self):
		self.next_minion_in = 0
		self.offset_wave = 0
		self.offset_minion = 0
		self.nr_minion = 0
		self.hp_minion = 0
		
	def update(self, delta):
		self.next_minion_in -= delta
		if self.next_minion_in <= 0:
			self.new_minion = True
			self.next_minion_in = self.offset_minion
			
		

class ScreenObject:
	"""An Object that appears on screen"""
	x = 0
	y = 0
	def __init__(self):
		pass

class MovingObject(ScreenObject):
	"""A moving object"""
	dx = 0
	dy = 0
	def __init__(self):
		ScreenObject.__init__(self)

class Tower(ScreenObject):
	"""A tower shooting bullets"""
	next_shoot_in = 0
	firing_range = 5
	speed = 3

	def create_bullet(self, minion):
		"""Creates a bullet object heading towards a minion 
		and returns that object.
		"""
		bullet =  Bullet()
		time = self.vorhalt(minion, bullet)
		bullet.x = float(self.x)
		bullet.y = float(self.y)

		diff_x = (minion.x + time * minion.dx) - bullet.x
		diff_y = (minion.y + time * minion.dy) - bullet.y

		dist = math.sqrt( diff_x * diff_x + diff_y * diff_y )

		bullet.dx = bullet.speed * float(diff_x) / float(dist)
		bullet.dy = bullet.speed * float(diff_y) / float(dist)

		return bullet

	def vorhalt(self, minion, bullet):
		"""Computes the time when the bullet reaches the minion."""
		a = minion.dx * minion.dx + minion.dy * minion.dy - \
			bullet.speed * bullet.speed
		b = 2 * (minion.x - self.x) * minion.dx + 2*(minion.y - self.y) * minion.dy
		c = math.pow( minion.x - self.x , 2) + math.pow( minion.y - self.y, 2)

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
			diff_x = self.x - minion.x
			diff_y = self.y - minion.y

			dist = math.sqrt( diff_x * diff_x + diff_y * diff_y )

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
	x = 5
	y = 1
	speed = 1
	current_wp = 1
	waypoints = None

	def __init__(self, waypoints):
		MovingObject.__init__(self)
		self.waypoints = waypoints

	def animate(self, delta):
		"""Computes new position."""
		#TODO: negative dx erlauben
		current_waypoint = self.waypoints[self.current_wp]
		diff_x = abs(self.x - current_waypoint[0])
		diff_y = abs(self.y - current_waypoint[1])
		if diff_x > diff_y:
			dist_to_cw = diff_x
		else:
			dist_to_cw = diff_y

		if dist_to_cw < delta*self.speed: # go to next wp
			way_to_go = delta*self.speed - dist_to_cw
			self.x = current_waypoint[0]
			self.y = current_waypoint[1]
			self.current_wp += 1
			if self.current_wp < len(self.waypoints):
				current_waypoint = self.waypoints[self.current_wp]
				diff_x = abs(self.x - current_waypoint[0])
				diff_y = abs(self.y - current_waypoint[1])
			else:
				end_reached = True
				diff_x = 0
				diff_y = 0
				way_to_go = 0
		else:
			way_to_go = delta*self.speed
		if diff_x > diff_y:
			self.x += way_to_go
			self.dx = self.speed
			self.dy = 0
		else:
			self.y += way_to_go		
			self.dx = 0
			self.dy = self.speed


class Bullet(MovingObject):
	"""A bullet flying down a straight line."""
	speed = 1.5

	def animate(self, delta):
		"""Computes new position."""
		self.x += delta * self.dx
		self.y += delta * self.dy


class Logic:
	"""Holds the game logic."""
	minions = []
	bullets = []
	towers = []
	current_level = None
	money = None
	points = None
	lives = None

	def __init__(self):
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
								if tower.x == x: 
									if tower.y == y:
										return
							tower = Tower()
							tower.x = x
							tower.y = y
							self.towers.append(tower)

	def add_minion(self):
		"""Adds minion on beginning of the pathway."""
		self.minions.append(Minion(self.current_level.waypoints))

	def check_for_finished_minions(self):
		"""Check if minion reached end of pathway."""
		for minion in self.minions[:]:
			if minion.current_wp == len(minion.waypoints):
				self.lives -= 1
				self.minions.remove(minion)

	def collision_detection(self):
		"""Checks if bullet reached a minion. If yes, both are deleted."""
		for bullet in self.bullets:
			if int(bullet.x) < 1:
				self.bullets.remove(bullet)
				continue
			if int(bullet.x) > self.current_level.max_x:
				self.bullets.remove(bullet)
				continue
			if int(bullet.y) < 1:
				self.bullets.remove(bullet)
				continue
			if int(bullet.y) > self.current_level.max_y:
				self.bullets.remove(bullet)
				continue
			for minion in self.minions:
				if int(bullet.x) == int(minion.x):
					if int(bullet.y) == int(minion.y):
						self.bullets.remove(bullet)
						self.minions.remove(minion)
						self.points += 1
						self.money += 1
						break

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
		for w in self.current_level.active_waves[:]:
			if w.new_minion:
				w.new_minion = False
				w.nr_minion -= 1
				self.add_minion()
				if w.nr_minion == 0:
					self.current_level.active_waves.remove(w)
				
		


