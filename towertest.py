from logic import Tower, Bullet, Minion
from vector import Vector
import unittest

class Vorhalt(unittest.TestCase):
    def test1(self):
        for x2 in range(1, 100):
            for x1 in range(1, 100):
                t = Tower(Vector(x1, x2))
                b = Bullet(t.pos)
                wp = {}
                wp[0] = Vector(100, 6)
                wp[1] = Vector(6, 100)
                m = Minion(wp, 10)

                res = t.vorhalt(m, b)
                
                m.animate(res)
                #delta = 1
                #print(str(t.pos) + "  " + str(res))
                #print(str(m.pos))
                self.failUnlessAlmostEqual(m.pos.Distance(t.pos), b.speed * res, 12)
    
if __name__ == "__main__":
    unittest.main() 
