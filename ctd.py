import curses, sys, traceback, time, logic


# global variables
class gb:
	scrn = None # will point to window object
	mapping = {}
	current_time = 0
	last_time = 0
	delta = current_time - last_time


def draw_minions():
	for m in logic.minions:
		draw_at(int(m.x),int(m.y),'o', curses.COLOR_BLACK, curses.COLOR_YELLOW)

def draw_bullets():
	for b in logic.bullets:
		if logic.a_map.tiles[int(b.x),int(b.y)] == 0:
			draw_at(int(b.x),int(b.y),'*', curses.COLOR_BLACK, curses.COLOR_GREEN)
		else:
			draw_at(int(b.x),int(b.y),'*', curses.COLOR_BLACK, curses.COLOR_YELLOW)




def draw_towers():
	for t in logic.towers:
		draw_at(int(t.x),int(t.y),'#', curses.COLOR_BLACK, curses.COLOR_GREEN)

def draw_map():
	for x in range(1,21):
		for y in range(1,21):
			if logic.a_map.tiles[x,y] == 0:
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

	gb.scrn.keypad(1)

	gb.scrn.nodelay(1)
	# start color display (if it exists; could check with has_colors())
	curses.start_color()

	curses.mousemask(curses.BUTTON1_PRESSED)

	# clear screen
	gb.scrn.clear()


	list_of_colors = [ curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_WHITE, curses.COLOR_YELLOW  ]

	i = 1;
	for bg in list_of_colors:
		for fg in list_of_colors:
			curses.init_pair(i,fg,bg)
			gb.mapping[fg,bg] = i
			i+=1

	logic.init_map()

	last_time = time.time()
	current_time =  time.time()

	# implement the actions done so far (just the clear())
	gb.scrn.refresh()

	while True:
		# read character from keyboard
		c = gb.scrn.getch()
		# was returned as an integer (ASCII); make it a character
		if c != -1:
			if c == curses.KEY_MOUSE:
				id,y,x,z,button = curses.getmouse()
				if x >= 1 :
					if x <= logic.a_map.max_x : 
						if y >= 1 :
							if y <= logic.a_map.max_y:
								if logic.a_map.tiles[x,y] == 0:
									nt = logic.tower()
									nt.x = x
									nt.y = y
									logic.towers.append(nt)
			else:
				c = chr(c)
				# quit?
				if c == 'q': break
				if c == 'a':
					logic.minions.append(logic.minion())
		gb.last_time = gb.current_time
		gb.current_time = time.time()
		gb.delta = gb.current_time - gb.last_time
		logic.collision_detection()
		for m in logic.minions:
			m.animate(gb.delta)
		for t in logic.towers:
			t.animate(gb.delta)
		for b in logic.bullets:
			b.animate(gb.delta)
		draw_map()
		draw_minions()
		draw_towers()
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

