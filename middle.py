import logic, time
from xml.dom import minidom
from system import System

system = System()
restore = system.restorescreen

# global variables
class gb:
	current_time = 0
	last_time = 0
	delta = current_time - last_time


def draw_minions():
	for m in logic.minions:
		system.draw_at(int(m.x),int(m.y),'o', system.COLOR_BLACK, system.COLOR_YELLOW)

def draw_bullets():
	for b in logic.bullets:
		if logic.current_level.tiles[int(b.x),int(b.y)] == 0:
			system.draw_at(int(b.x),int(b.y),'*', system.COLOR_BLACK, system.COLOR_GREEN)
		else:
			system.draw_at(int(b.x),int(b.y),'*', system.COLOR_BLACK, system.COLOR_YELLOW)

def draw_towers():
	for t in logic.towers:
		system.draw_at(int(t.x),int(t.y),'#', system.COLOR_BLACK, system.COLOR_GREEN)

def draw_map():
	for x in range(1,21):
		for y in range(1,21):
			if logic.current_level.tiles[x,y] == 0:
				system.draw_at(x,y,' ', system.COLOR_GREEN, system.COLOR_GREEN)
			else:
				system.draw_at(x,y,' ', system.COLOR_YELLOW, system.COLOR_YELLOW)

def load_map(file_name):
	map_xml = minidom.parse(file_name)

	map_tag = map_xml.getElementsByTagName('map')


	nl = logic.level()
	nl.max_y = int( map_tag[0].getElementsByTagName('rows')[0].firstChild.data )
	nl.max_x = int( map_tag[0].getElementsByTagName('columns')[0].firstChild.data )

	row_tag = map_xml.getElementsByTagName('row')

	for r in row_tag:
		s = r.firstChild.data
		y = int(r.attributes['pos'].value)
		for x in range(1,len(s)+1):
			nl.tiles[x,y] = int(s[x-1])

	wps_tag = map_xml.getElementsByTagName('waypoints')[0].getElementsByTagName('waypoint')

	for wp in wps_tag:	
		nr = int( wp.attributes['nr'].value )
		x = int( wp.getElementsByTagName('x')[0].firstChild.data )
		y = int( wp.getElementsByTagName('y')[0].firstChild.data )

		nl.waypoints[nr] = [x,y]

	return nl

def init():
	logic.current_level = load_map('map.xml')

	last_time = time.time()
	current_time =  time.time()


def run():
	while True:
		# read character from keyboard
		c = system.getch()
		# was returned as an integer (ASCII); make it a character
		if c != -1:
			if c == system.KEY_MOUSE:
				id,x,y,z,button = system.getmouse()
				logic.add_tower(x,y)
			else:
				c = chr(c)
				# quit?
				if c == 'q': break
				if c == 'a':
					logic.add_minion()
		gb.last_time = gb.current_time
		gb.current_time = time.time()
		gb.delta = gb.current_time - gb.last_time
		logic.animate(gb.delta)
		draw_map()
		draw_minions()
		draw_towers()
		draw_bullets()

	# restore original settings
	system.restorescreen()
