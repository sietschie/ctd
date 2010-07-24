import curses, sys

scrn = None # will point to window object
mapping = {}
list_of_colors = [ curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_WHITE, curses.COLOR_YELLOW  ]
KEY_MOUSE = curses.KEY_MOUSE
COLOR_BLACK = curses.COLOR_BLACK
COLOR_GREEN = curses.COLOR_GREEN
COLOR_YELLOW = curses.COLOR_YELLOW
getch = None
getmouse = curses.getmouse

def draw_at(x,y,chr,fg,bg):
	scrn.addch(y,x,chr,curses.color_pair(mapping[fg,bg]))

def init():
	# first we must create a window object; it will fill the whole screen
	global scrn
	scrn = curses.initscr()
	# turn off keystroke echo
	curses.noecho()
	# keystrokes are honored immediately, rather than waiting for the
	# user to hit Enter
	curses.cbreak()

	scrn.keypad(1)

	scrn.nodelay(1)
	# start color display (if it exists; could check with has_colors())
	curses.start_color()

	curses.mousemask(curses.BUTTON1_PRESSED)

	global getch
	getch = scrn.getch

	# clear screen
	scrn.clear()

	i = 1;
	for bg in list_of_colors:
		for fg in list_of_colors:
			curses.init_pair(i,fg,bg)
			mapping[fg,bg] = i
			i+=1

	# implement the actions done so far (just the clear())
	scrn.refresh()



# this code is vital; without this code, your terminal would be unusable
# after the program exits
def restorescreen():
	# restore "normal"--i.e. wait until hit Enter--keyboard mode
	curses.nocbreak()
	# restore keystroke echoing
	curses.echo()
	# required cleanup call
	curses.endwin()


