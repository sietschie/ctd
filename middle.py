import time
from xml.dom import minidom
from system import System
from logic import Logic, Level


# global variables
class Middle:
	current_time = 0
	last_time = 0
	delta = current_time - last_time

	system = System()
	logic = Logic()
	restore = system.restorescreen


	def draw_minions(self):
		for minion in self.logic.minions:
			self.system.draw_at(int(minion.x), int(minion.y), 'o', 
				self.system.COLOR_BLACK, self.system.COLOR_YELLOW)

	def draw_bullets(self):
		for bullet in self.logic.bullets:
			if self.logic.current_level.tiles[int(bullet.x), int(bullet.y)] == 0:
				self.system.draw_at(int(bullet.x), int(bullet.y), '*', 
					self.system.COLOR_BLACK, self.system.COLOR_GREEN)
			else:
				self.system.draw_at(int(bullet.x), int(bullet.y), '*', 
					self.system.COLOR_BLACK, self.system.COLOR_YELLOW)

	def draw_towers(self):
		for tower in self.logic.towers:
			self.system.draw_at(int(tower.x), int(tower.y), '#', 
				self.system.COLOR_BLACK, self.system.COLOR_GREEN)

	def draw_map(self):
		for x in range(1, 21):
			for y in range(1, 21):
				if self.logic.current_level.tiles[x, y] == 0:
					self.system.draw_at(x, y, ' ', 
						self.system.COLOR_GREEN, self.system.COLOR_GREEN)
				else:
					self.system.draw_at(x, y, ' ', 
						self.system.COLOR_YELLOW, self.system.COLOR_YELLOW)

	def load_map(self, file_name):
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

		self.logic.current_level = level

	def __init__(self):
		self.load_map('map.xml')

		self.last_time = time.time()
		self.current_time =  time.time()


	def run(self):
		while True:
			# read character from keyboard
			char = self.system.getch()
			# was returned as an integer (ASCII); make it a character
			if char != -1:
				if char == self.system.KEY_MOUSE:
					device_id, x, y, z, button = self.system.getmouse()
					self.logic.add_tower(x, y)
				else:
					char = chr(char)
					# quit?
					if char == 'q': 
						break
					if char == 'a':
						self.logic.add_minion()
			self.last_time = self.current_time
			self.current_time = time.time()
			self.delta = self.current_time - self.last_time
			self.logic.animate(self.delta)
			self.draw_map()
			self.draw_minions()
			self.draw_towers()
			self.draw_bullets()

		# restore original settings
		self.system.restorescreen()
