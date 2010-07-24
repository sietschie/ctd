import math

minions = []
bullets = []
towers = []
current_level = None

class ScreenObject:
	x = 0
	y = 0

class MovingObject(ScreenObject):
	dx = 0
	dy = 0

class tower(ScreenObject):
	next_shoot_in = 0
	speed = 3

	def shoot(self, cm):
		t = self.vorhalt(cm)
		nb =  bullet()
		nb.x = float(self.x)
		nb.y = float(self.y)

		diff_x = (cm.x + t * cm.dx) - nb.x
		diff_y = (cm.y + t * cm.dy) - nb.y
	
		dist = math.sqrt( diff_x * diff_x + diff_y * diff_y )

		nb.dx = nb.speed * float(diff_x) / float(dist)
		nb.dy = nb.speed * float(diff_y) / float(dist)

		bullets.append(nb)

	def vorhalt(self, cm):
		a = cm.dx * cm.dx + cm.dy * cm.dy - bullet.speed * bullet.speed;
		b = 2 * (cm.x - self.x) * cm.dx + 2*(cm.y - self.y) * cm.dy;
		c = math.pow( cm.x - self.x , 2) + math.pow( cm.y - self.y, 2);

		if a == 0: #vllt mit epsilon?
			t = -c / b;

		else: # fuer speed ungleich 1, nicht getestet.
			t1 = ( - b + math.sqrt( b * b - 4 * a * c))/(2*a);
			t2 = ( - b - math.sqrt( b * b - 4 * a * c))/(2*a);

			if t1 > 0:
				if t2 > 0:
					t = min(t1,t2)
				else:
					t = t1
			else:
				if t2 > 0:
					t = t2
				#else:
					# irgendnen fehler?			
		return t
	
	
	def find_target(self):
		min_dist = 100000
		min_min = 0
		for m in minions:
			diff_x = self.x - m.x
			diff_y = self.y - m.y

			dist = math.sqrt( diff_x * diff_x + diff_y * diff_y )

			if dist < min_dist:
				min_dist = dist
				min_min = m

		if min_dist < 5:
			return min_min
		else:
			return 0

	def animate(self, delta):
		self.next_shoot_in -= delta
		if self.next_shoot_in < 0: 
			m = self.find_target()

			if m != 0:
				self.shoot(m)	
				self.next_shoot_in = self.speed

class minion(MovingObject):
	x = 5
	y = 1
	speed = 1
	current_wp = 1

	def animate(self, delta):
		cw = current_level.waypoints[self.current_wp]
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
			cw = current_level.waypoints[self.current_wp]
			diff_x = self.x - cw[0]
			diff_y = self.y - cw[1]
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
		if int(self.x) < 1:
			minions.remove(self)
		if int(self.x) > current_level.max_x:
			minions.remove(self)
		if int(self.y) < 1:
			minions.remove(self)
		if int(self.y) > current_level.max_y:
			minions.remove(self)


class bullet(MovingObject):
	speed = 1.5

	def animate(self, delta):
		self.x += delta * self.dx
		self.y += delta * self.dy
		if int(self.x) < 1:
			bullets.remove(self)
		if int(self.x) > current_level.max_x:
			bullets.remove(self)
		if int(self.y) < 1:
			bullets.remove(self)
		if int(self.y) > current_level.max_y:
			bullets.remove(self)

def add_tower(x,y):
	if x >= 1 :
		if x <= current_level.max_x : 
			if y >= 1 :
				if y <= current_level.max_y:
					if current_level.tiles[x,y] == 0:
						nt = tower()
						nt.x = x
						nt.y = y
						towers.append(nt)

def add_minion():
	minions.append(minion())


def collision_detection():
	for b in bullets:
		for m in minions:
			if int(b.x) == int(m.x):
				if int(b.y) == int(m.y):
					bullets.remove(b)
					minions.remove(m)

def animate(delta):
	collision_detection()
	for m in minions:
		m.animate(delta)
	for t in towers:
		t.animate(delta)
	for b in bullets:
		b.animate(delta)


class level:
	tiles = {}
	max_x = 0
	max_y = 0
	waypoints = {}
