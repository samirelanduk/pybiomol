import math

class Atom:

    def __init__(self, element, atom_id, x, y, z, name=None):
        self.element = element.title()
        self.atom_id = atom_id
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.name = name if name else element


    def __repr__(self):
        return "<%s Atom>" % self.element


    def distance_to(self, other_object):
        x_sum = math.pow((other_object.x - self.x), 2)
        y_sum = math.pow((other_object.y - self.y), 2)
        z_sum = math.pow((other_object.z - self.z), 2)
        distance = math.sqrt(x_sum + y_sum + z_sum)
        return distance
