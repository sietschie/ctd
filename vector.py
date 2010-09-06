import math

class Vector:
    'Represents a 2D vector.'
    def __init__(self, x = 0, y = 0):
        self.x = float(x)
        self.y = float(y)
        
    def __add__(self, val):
        return Vector( self[0] + val[0], self[1] + val[1] )
    
    def __sub__(self,val):
        return Vector( self[0] - val[0], self[1] - val[1] )
    
    def __iadd__(self, val):
        #self.x = val[0] + self.x
        #self.y = val[1] + self.y
        #return self
        return Vector( self[0] + val[0], self[1] + val[1] )

    def __isub__(self, val):
        self.x = self.x - val[0]
        self.y = self.y - val[1]
        return self
    
    def __div__(self, val):
        return Point( self[0] / val, self[1] / val )
    
    def __mul__(self, val):
        return Vector( self[0] * val, self[1] * val )
    
    def __idiv__(self, val):
        self[0] = self[0] / val
        self[1] = self[1] / val
        return self

    def __imul__(self, val):
        self[0] = self[0] * val
        self[1] = self[1] * val
        return self
                
    def __getitem__(self, key):
        if( key == 0):
            return self.x
        elif( key == 1):
            return self.y
        else:
            raise Exception("Invalid key to Point")

    def __setitem__(self, key, value):
        if( key == 0):
            self.x = value
        elif( key == 1):
            self.y = value
        else:
            raise Exception("Invalid key to Point")
        
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def to_int(self):
        return Vector(int(self.x), int(self.y))
        
    def abs(self):
        return Vector(abs(self.x), abs(self.y))

    def DistanceSqrd( point1, point2 ):
        'Returns the distance between two points squared. Marginally faster than Distance()'
        return ( (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

    def Distance( point1, point2 ):
        'Returns the distance between two points'
        return math.sqrt( point1.DistanceSqrd(point2) )

    def get_length(self):
        return math.sqrt( self[0]**2 + self[1]**2)
        
    def set_length(self, length):
        mul = length / self.get_length()
        self *= mul
        return self
