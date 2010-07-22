import curses, sys, traceback

# global variables
class gb:
	scrn = None # will point to window object

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
	# clear screen
	gb.scrn.clear()
	# implement the actions done so far (just the clear())
	gb.scrn.refresh()

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

