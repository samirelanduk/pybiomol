class Atom:

    def __init__(self, element, atom_id, x, y, z, name=None):
        self.element = element
        self.atom_id = atom_id
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.name = name if name else element
