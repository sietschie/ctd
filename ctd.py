import curses, sys, traceback

# global variables
class gb:
	scrn = None # will point to window object
	mapping = {}
	the_map = {}

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

	# implement the actions done so far (just the clear())
	gb.scrn.refresh()

	draw_map()
	# wait for key to be pressed
	gb.scrn.getch()

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

