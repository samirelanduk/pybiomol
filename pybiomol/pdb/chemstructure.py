class Atom:

    def __init__(self, element, atom_id, x, y, z, name=None):
        self.element = element
        self.atom_id = atom_id
        self.x = x
        self.y = y
        self.z = z
        self.name = name if name else element
