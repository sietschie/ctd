import curses, sys, traceback, time, math

class tower:
	x = 12
	y = 8
	last_shoot = 0
	speed = 3

# global variables
class gb:
	scrn = None # will point to window object
	mapping = {}
	the_map = {}
	waypoints = {}
	current_time = 0
	last_time = 0
	minions = []
	tower = tower()
	bullets = []
	max_x = 20
	max_y = 20

class minion:
	x = 1
	y = 5
	dx = 0
	dy = 0
	speed = 1
	current_wp = 1

class bullet:
	x = 0
	y = 0
	dx = 0
	dy = 0
	speed = 1.5



def draw_minions():
	for m in gb.minions:
		draw_at(int(m.x),int(m.y),'o', curses.COLOR_BLACK, curses.COLOR_YELLOW)

def draw_bullets():
	for b in gb.bullets:
		if gb.the_map[int(b.x),int(b.y)] == 0:
			draw_at(int(b.x),int(b.y),'*', curses.COLOR_BLACK, curses.COLOR_GREEN)
		else:
			draw_at(int(b.x),int(b.y),'*', curses.COLOR_BLACK, curses.COLOR_YELLOW)

def animate_bullets():
	delta = gb.current_time - gb.last_time
	for b in gb.bullets:
		b.x += delta * b.dx
		b.y += delta * b.dy
		if int(b.x) < 1:
			gb.bullets.remove(b)
		if int(b.x) > gb.max_x:
			gb.bullets.remove(b)
		if int(b.y) < 1:
			gb.bullets.remove(b)
		if int(b.y) > gb.max_y:
			gb.bullets.remove(b)

def collision_detection():
	for b in gb.bullets:
		for m in gb.minions:
			if int(b.x) == int(m.x):
				if int(b.y) == int(m.y):
					gb.bullets.remove(b)
					gb.minions.remove(m)

def shoot(ct, cm):
	t = vorhalt(ct,cm)
	nb =  bullet()
	nb.x = float(ct.x)
	nb.y = float(ct.y)

	diff_x = (cm.x + t * cm.dx) - nb.x
	diff_y = (cm.y + t * cm.dy) - nb.y
	
	dist = math.sqrt( diff_x * diff_x + diff_y * diff_y )

	nb.dx = nb.speed * float(diff_x) / float(dist)
	nb.dy = nb.speed * float(diff_y) / float(dist)

	gb.bullets.append(nb)

def vorhalt(ct, cm):
	a = cm.dx * cm.dx + cm.dy * cm.dy - bullet.speed * bullet.speed;
	b = 2 * (cm.x - ct.x) * cm.dx + 2*(cm.y - ct.y) * cm.dy;
	c = math.pow( cm.x - ct.x , 2) + math.pow( cm.y - ct.y, 2);

	if a == 0: #vllt mit epsilon?
		t = -c / b;
		gb.scrn.addstr(20,20,str( t ))
		gb.scrn.addstr(21,21,str( b ))
		gb.scrn.addstr(22,22,str( c ))
		gb.scrn.addstr(23,23,str( cm.dy ))
		gb.scrn.addstr(24,24,str( ct.y ))
		gb.scrn.addstr(25,25,str( cm.y ))
		gb.scrn.addstr(26,26,str( cm.dx ))
		gb.scrn.addstr(27,27,str( ct.x ))
		gb.scrn.addstr(28,28,str( cm.x ))

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
	
	
def find_target(ct):
	min_dist = 100000
	min_min = 0
	for m in gb.minions:
		diff_x = ct.x - m.x
		diff_y = ct.y - m.y
	
		dist = math.sqrt( diff_x * diff_x + diff_y * diff_y )

		if dist < min_dist:
			min_dist = dist
			min_min = m

	if min_dist < 5:
		return min_min
	else:
		return 0

def animate_tower():
	if gb.current_time - gb.tower.last_shoot > gb.tower.speed: 
		m = find_target(gb.tower)

		if m != 0:
			shoot(gb.tower, m)	
			gb.tower.last_shoot = gb.current_time

def animate_minions():
	delta = gb.current_time - gb.last_time
	for m in gb.minions:
		cw = gb.waypoints[m.current_wp]
		diff_x = abs(m.x - cw[0])
		diff_y = abs(m.y - cw[1])
		if diff_x > diff_y:
			dist_to_cw = diff_x
		else:
			dist_to_cw = diff_y

		if dist_to_cw < delta*m.speed: # go to next wp
			way_to_go = delta*m.speed - dist_to_cw
			m.x = cw[0]
			m.y = cw[1]
			m.current_wp += 1
			cw = gb.waypoints[m.current_wp]
			diff_x = m.x - cw[0]
			diff_y = m.y - cw[1]
		else:
			way_to_go = delta*m.speed
		if diff_x > diff_y:
			m.x += way_to_go
			m.dx = way_to_go / delta
			m.dy = 0
		else:
			m.y += way_to_go		
			m.dx = 0
			m.dy = way_to_go / delta
		if int(m.x) < 1:
			gb.minions.remove(m)
		if int(m.x) > gb.max_x:
			gb.minions.remove(m)
		if int(m.y) < 1:
			gb.minions.remove(m)
		if int(m.y) > gb.max_y:
			gb.minions.remove(m)
def draw_tower():
	draw_at(int(gb.tower.x),int(gb.tower.y),'#', curses.COLOR_BLACK, curses.COLOR_GREEN)

def draw_map():
	for x in range(1,21):
		for y in range(1,21):
			if gb.the_map[x,y] == 0:
				draw_at(x,y,' ', curses.COLOR_GREEN, curses.COLOR_GREEN)
			else:
				draw_at(x,y,' ', curses.COLOR_YELLOW, curses.COLOR_YELLOW)

def draw_at(x,y,chr,fg,bg):
	gb.scrn.addch(x,y,chr,curses.color_pair(gb.mapping[fg,bg]))

# this code is vital; without this code, your terminal would be unusable
# after the program exits
def restorescreen():
	# restore "normal"--i.e. wait until hit Enter--keyboard mode
	curses.nocbreak()
	# restore keystroke echoing
	curses.echo()
	# required cleanup call
	curses.endwin()

def main():
	# first we must create a window object; it will fill the whole screen
	gb.scrn = curses.initscr()
	# turn off keystroke echo
	curses.noecho()
	# keystrokes are honored immediately, rather than waiting for the
	# user to hit Enter
	curses.cbreak()

	gb.scrn.nodelay(1)
	# start color display (if it exists; could check with has_colors())
	curses.start_color()
	# clear screen
	gb.scrn.clear()


	list_of_colors = [ curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_WHITE, curses.COLOR_YELLOW  ]

	i = 1;
	for bg in list_of_colors:
		for fg in list_of_colors:
			curses.init_pair(i,fg,bg)
			gb.mapping[fg,bg] = i
			i+=1

	#init map
	for x in range(1,21):
		for y in range(1,21):
			gb.the_map[x,y] = 0; #todo: durch konstante ersetzen

	for x in range(1,15):
			gb.the_map[x,5] = 1;

	for y in range(5,21	):
			gb.the_map[15,y] = 1;

	gb.waypoints[0] = [0,5]
	gb.waypoints[1] = [15,5]
	gb.waypoints[2] = [15,22]

	last_time = time.time()
	current_time =  time.time()

	# implement the actions done so far (just the clear())
	gb.scrn.refresh()

	while True:
		# read character from keyboard
		c = gb.scrn.getch()
		# was returned as an integer (ASCII); make it a character
		if c != -1:
			i = c
			c = chr(c)
			# quit?
			if c == 'q': break
			if c == 'a':
				gb.minions.append(minion())
		gb.last_time = gb.current_time
		gb.current_time = time.time()
		collision_detection()
		animate_minions()
		animate_tower()
		animate_bullets()
		draw_map()
		draw_minions()
		draw_tower()
		draw_bullets()

	# restore original settings
	restorescreen()

if __name__ =='__main__':
	# in case of execution error, have a smooth recovery and clear
	# display of error message (nice example of Python exception
	# handling); it is recommended that you use this format for all of
	# your Python curses programs; you can automate all this (and more)
	# by using the built-in function curses.wrapper(), but we've shown
	# it done "by hand" here to illustrate the issues involved
	try:
		main()
	except:
		restorescreen()
		# print error message re exception
		traceback.print_exc()

