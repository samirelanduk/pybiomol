from .chemstructure import *

class Residue(Molecule):

    def __init__(self, name, atoms):
        self.name = name
        Molecule.__init__(self, *atoms)


    def __repr__(self):
        return "<Residue (%s)>" % self.name



class ResiduicStructure(AtomicStructure):

    def __init__(self, residues):
        self.residues = residues
        atoms = []
        for residue in self.residues:
            atoms += residue.atoms
        AtomicStructure.__init__(self, *atoms)


    def __repr__(self):
        return "<ResiduicStructure (%i residues)>" % len(self.residues)
