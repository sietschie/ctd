import curses

class System:
	scrn = None # will point to window object
	mapping = {}
	list_of_colors = [ curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_CYAN,
	curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_WHITE,
	curses.COLOR_YELLOW  ]
	KEY_MOUSE = curses.KEY_MOUSE
	COLOR_BLACK = curses.COLOR_BLACK
	COLOR_GREEN = curses.COLOR_GREEN
	COLOR_YELLOW = curses.COLOR_YELLOW
	getch = None
	getmouse = curses.getmouse

	def draw_at(self, coord_x, coord_y, char, color_fg, color_bg):
		self.scrn.addch(coord_y, coord_x, char, \
			curses.color_pair(self.mapping[color_fg, color_bg]))

	def __init__(self):
		# first we must create a window object; it will fill the whole screen
		self.scrn = curses.initscr()
		# turn off keystroke echo
		curses.noecho()
		# keystrokes are honored immediately, rather than waiting for the
		# user to hit Enter
		curses.cbreak()

		self.scrn.keypad(1)

		self.scrn.nodelay(1)
		# start color display (if it exists; could check with has_colors())
		curses.start_color()

		curses.mousemask(curses.BUTTON1_PRESSED)

		self.getch = self.scrn.getch

		# clear screen
		self.scrn.clear()

		i = 1
		for color_background in self.list_of_colors:
			for color_foreground in self.list_of_colors:
				curses.init_pair(i, color_foreground, color_background)
				self.mapping[color_foreground, color_background] = i
				i += 1

		# implement the actions done so far (just the clear())
		self.scrn.refresh()



	# this code is vital; without this code, your terminal would be unusable
	# after the program exits
	@staticmethod
	def restorescreen():
		# restore "normal"--i.e. wait until hit Enter--keyboard mode
		curses.nocbreak()
		# restore keystroke echoing
		curses.echo()
		# required cleanup call
		curses.endwin()


