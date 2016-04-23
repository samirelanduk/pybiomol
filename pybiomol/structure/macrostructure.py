from .chemstructure import *

class Residue(Molecule):

    def __init__(self, name, atoms):
        self.name = name
        Molecule.__init__(self, *atoms)


    def __repr__(self):
        return "<Residue (%s)>" % self.name
