import time, logic, system, traceback


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
		if logic.a_map.tiles[int(b.x),int(b.y)] == 0:
			system.draw_at(int(b.x),int(b.y),'*', system.COLOR_BLACK, system.COLOR_GREEN)
		else:
			system.draw_at(int(b.x),int(b.y),'*', system.COLOR_BLACK, system.COLOR_YELLOW)




def draw_towers():
	for t in logic.towers:
		system.draw_at(int(t.x),int(t.y),'#', system.COLOR_BLACK, system.COLOR_GREEN)

def draw_map():
	for x in range(1,21):
		for y in range(1,21):
			if logic.a_map.tiles[x,y] == 0:
				system.draw_at(x,y,' ', system.COLOR_GREEN, system.COLOR_GREEN)
			else:
				system.draw_at(x,y,' ', system.COLOR_YELLOW, system.COLOR_YELLOW)



def main():
	system.init()

	logic.init_map()

	last_time = time.time()
	current_time =  time.time()

	while True:
		# read character from keyboard
		c = system.getch()
		# was returned as an integer (ASCII); make it a character
		if c != -1:
			if c == system.KEY_MOUSE:
				id,y,x,z,button = system.getmouse()
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
		system.restorescreen()
		# print error message re exception
		traceback.print_exc()

