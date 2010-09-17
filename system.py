"""Handles communication with the system"""
import curses
from vector import Vector
from events import KeyPressEvent, MouseClickEvent, ClearScreenEvent, TickEvent

class System:
    """Handles communication with the system"""
    scrn = None # will point to window object
    mapping = {}
    list_of_colors = [ curses.COLOR_BLACK, curses.COLOR_BLUE, 
    curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_MAGENTA, 
    curses.COLOR_RED, curses.COLOR_WHITE, curses.COLOR_YELLOW  ]
    COLOR_BLACK = curses.COLOR_BLACK
    COLOR_GREEN = curses.COLOR_GREEN
    COLOR_YELLOW = curses.COLOR_YELLOW

    def draw_at(self, coord, char, color_fg, color_bg):
        """puts char to screen"""
        self.scrn.addch(int(coord.y), int(coord.x), char, \
            curses.color_pair(self.mapping[color_fg, color_bg]))
            
    def draw_string_at(self, coord_x, coord_y, string):
        """puts string to screen"""
        self.scrn.addstr(coord_y, coord_x, string)
        
    def update(self):
        char = self.scrn.getch()
        # was returned as an integer (ASCII); make it a character
        if char != -1:
            if char == curses.KEY_MOUSE:
                #device_id, x, y, z, button = self.system.getmouse()
                ret = curses.getmouse()
                x = ret[1]
                y = ret[2]
                button = ret[4]
                self.evm.Post(MouseClickEvent(button, Vector(x, y)))
            else:
                char = chr(char)
                self.evm.Post(KeyPressEvent(char))

    def Notify(self, event):
        if isinstance( event, ClearScreenEvent ):
            self.scrn.erase()
        elif isinstance( event, TickEvent ):
            self.update()

    def __init__(self, evm):
        self.evm = evm
        evm.RegisterListener(self)
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

        curses.curs_set(0)

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
        """gets terminal back to normal state"""
        # restore "normal"--i.e. wait until hit Enter--keyboard mode
        curses.nocbreak()
        # restore keystroke echoing
        curses.echo()
        # required cleanup call
        curses.endwin()


