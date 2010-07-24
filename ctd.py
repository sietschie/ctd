import middle, traceback

def main():
	middle.init()
	middle.run()


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
		middle.restore()
		# print error message re exception
		traceback.print_exc()

