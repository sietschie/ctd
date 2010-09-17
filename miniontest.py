from logic import Minion
from vector import Vector
import math
import unittest

class TestWaypoints(unittest.TestCase):
    def test_waypoints(self):
        'test if minion correctly walks along all the waypoints'
        for steps in range(1,101):
            wp = {}
            wp[0] = Vector(1,0)
            wp[1] = Vector(0,1)
            wp[2] = Vector(0,2)
            wp[3] = Vector(1,3)
            wp[4] = Vector(2,3)
            wp[5] = Vector(3,2)
            wp[6] = Vector(3,1)
            wp[7] = Vector(2,0)
            wp[8] = Vector(1,0)
            
            distance = 4 + 4 * math.sqrt(2)
            
            m = Minion(wp,10)
            #TODO: minion speed auf 1 setzen
            for step in range(0,steps) :
                old = m.pos
                m.animate(distance / steps)
                new = m.pos
                self.failIf(old.x == new.x and old.y == new.y, msg='minion did not move')

            self.failUnlessAlmostEqual(m.pos.x, wp[0].x, msg='minion did not reach the end position')
            self.failUnlessAlmostEqual(m.pos.y, wp[0].y, msg='minion did not reach the end position')
    
if __name__ == "__main__":
    unittest.main() 
