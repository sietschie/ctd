import math

minions = []
bullets = []
towers = []

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
	x = 1
	y = 5
	speed = 1
	current_wp = 1

	def animate(self, delta):
		cw = a_map.waypoints[self.current_wp]
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
			cw = a_map.waypoints[self.current_wp]
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
		if int(self.x) > a_map.max_x:
			minions.remove(self)
		if int(self.y) < 1:
			minions.remove(self)
		if int(self.y) > a_map.max_y:
			minions.remove(self)


class bullet(MovingObject):
	speed = 1.5

	def animate(self, delta):
		self.x += delta * self.dx
		self.y += delta * self.dy
		if int(self.x) < 1:
			bullets.remove(self)
		if int(self.x) > a_map.max_x:
			bullets.remove(self)
		if int(self.y) < 1:
			bullets.remove(self)
		if int(self.y) > a_map.max_y:
			bullets.remove(self)

def add_tower(x,y):
	if x >= 1 :
		if x <= a_map.max_x : 
			if y >= 1 :
				if y <= a_map.max_y:
					if a_map.tiles[x,y] == 0:
						nt = tower()
						nt.x = x
						nt.y = y
						towers.append(nt)


def collision_detection():
	for b in bullets:
		for m in minions:
			if int(b.x) == int(m.x):
				if int(b.y) == int(m.y):
					bullets.remove(b)
					minions.remove(m)

class a_map:
	tiles = {}
	max_x = 0
	max_y = 0
	waypoints = {}

def init_map():
	#init map
	for x in range(1,21):
		for y in range(1,21):
			a_map.tiles[x,y] = 0; #todo: durch konstante ersetzen

	for x in range(1,15):
			a_map.tiles[x,5] = 1;

	for y in range(5,21	):
			a_map.tiles[15,y] = 1;

	a_map.waypoints[0] = [0,5]
	a_map.waypoints[1] = [15,5]
	a_map.waypoints[2] = [15,22]

	a_map.max_x = 20
	a_map.max_y = 20
