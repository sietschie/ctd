import math

class Level:
	tiles = {}
	max_x = 0
	max_y = 0
	waypoints = {}

class ScreenObject:
	x = 0
	y = 0

class MovingObject(ScreenObject):
	dx = 0
	dy = 0

class Tower(ScreenObject):
	next_shoot_in = 0
	firing_range = 5
	speed = 3

	def create_bullet(self, minion):
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
		a = minion.dx * minion.dx + minion.dy * minion.dy - bullet.speed * bullet.speed
		b = 2 * (minion.x - self.x) * minion.dx + 2*(minion.y - self.y) * minion.dy
		c = math.pow( minion.x - self.x , 2) + math.pow( minion.y - self.y, 2)

		if a == 0: #vllt mit epsilon?
			t = -c / b

		else: # fuer speed ungleich 1, nicht getestet.
			t1 = ( - b + math.sqrt( b * b - 4 * a * c))/(2*a)
			t2 = ( - b - math.sqrt( b * b - 4 * a * c))/(2*a)

			if t1 > 0:
				if t2 > 0:
					t = min(t1, t2)
				else:
					t = t1
			else:
				if t2 > 0:
					t = t2
				#else:
					# irgendnen fehler?			
		return t


	def find_target(self, minions):
		min_dist = 100000
		min_min = 0
		for m in minions:
			diff_x = self.x - m.x
			diff_y = self.y - m.y

			dist = math.sqrt( diff_x * diff_x + diff_y * diff_y )

			if dist < min_dist:
				min_dist = dist
				min_min = m

		if min_dist < self.firing_range:
			return min_min
		else:
			return 0

	def animate(self, delta):
		self.next_shoot_in -= delta

	def shoot(self, minions):
		if self.next_shoot_in < 0: 
			m = self.find_target(minions)

			if m != 0:
				self.next_shoot_in = self.speed
				return self.create_bullet(m)	

class Minion(MovingObject):
	x = 5
	y = 1
	speed = 1
	current_wp = 1
	waypoints = None

	def __init__(self, waypoints):
		self.waypoints = waypoints

	def animate(self, delta):
		cw = self.waypoints[self.current_wp]
		diff_x = abs(self.x - cw[0])
		diff_y = abs(self.y - cw[1])
		if diff_x > diff_y:
			dist_to_cw = diff_x
		else:
			dist_to_cw = diff_y

		if dist_to_cw < delta*self.speed: # go to next wp
			way_to_go = delta*self.speed - dist_to_cw
			self.x = cw[0]
			self.y = cw[1]
			self.current_wp += 1
			if self.current_wp < len(self.waypoints):
				cw = self.waypoints[self.current_wp]
				diff_x = self.x - cw[0]
				diff_y = self.y - cw[1]
			else:
				diff_x = 0
				diff_y = 0
				way_to_go = 0
		else:
			way_to_go = delta*self.speed
		if diff_x > diff_y:
			self.x += way_to_go
			self.dx = way_to_go / delta
			self.dy = 0
		else:
			self.y += way_to_go		
			self.dx = 0
			self.dy = way_to_go / delta


class Bullet(MovingObject):
	speed = 1.5

	def animate(self, delta):
		self.x += delta * self.dx
		self.y += delta * self.dy


class Logic:
	minions = []
	bullets = []
	towers = []
	current_level = None

	def __init__(self):
		pass


	def add_tower(self, x, y):
		if x >= 1 :
			if x <= self.current_level.max_x : 
				if y >= 1 :
					if y <= self.current_level.max_y:
						if self.current_level.tiles[x, y] == 0:
							for t in self.towers:
								if t.x == x: 
									if t.y == y:
										return
							nt = Tower()
							nt.x = x
							nt.y = y
							self.towers.append(nt)

	def add_minion(self):
		self.minions.append(Minion(self.current_level.waypoints))

	def check_for_finished_minions(self):
		for minion in self.minions:
			if minion.current_wp == len(minion.waypoints):
				self.minions.remove(minion)

	def collision_detection(self):
		for b in self.bullets:
			if int(b.x) < 1:
				self.bullets.remove(b)
				continue
			if int(b.x) > self.current_level.max_x:
				self.bullets.remove(b)
				continue
			if int(b.y) < 1:
				self.bullets.remove(b)
				continue
			if int(b.y) > self.current_level.max_y:
				self.bullets.remove(b)
				continue
			for m in self.minions:
				if int(b.x) == int(m.x):
					if int(b.y) == int(m.y):
						self.bullets.remove(b)
						self.minions.remove(m)
						break

	def animate(self, delta):
		for m in self.minions:
			m.animate(delta)
		for t in self.towers:
			t.animate(delta)
		for b in self.bullets:
			b.animate(delta)
		self.check_for_finished_minions()
		self.collision_detection()
		for t in self.towers:
			bullet = t.shoot(self.minions)
			if bullet != None:
				self.bullets.append(bullet)
		


