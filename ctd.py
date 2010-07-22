import curses, sys, traceback, time

# global variables
class gb:
	scrn = None # will point to window object
	mapping = {}
	the_map = {}
	waypoints = {}
	current_time = 0
	last_time = 0
	minions = []
	max_x = 20
	max_y = 20

class minion:
	x = 1
	y = 5
	dx = 0
	dy = 0
	speed = 1
	current_wp = 1

def draw_minions():
	for m in gb.minions:
		draw_at(int(m.x),int(m.y),'o', curses.COLOR_BLACK, curses.COLOR_YELLOW)

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
		animate_minions()
		draw_map()
		draw_minions()

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

