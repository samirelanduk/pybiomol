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



class ResidueSequence(Molecule, ResiduicStructure):

    def __init__(self, residues):
        ResiduicStructure.__init__(self, residues)
        atoms = []
        for residue in self.residues:
            atoms += residue.atoms
        Molecule.__init__(self, *atoms)


    def __repr__(self):
        return "<ResidueSequence (%i residues)>" % len(self.residues)



class ProteinChain(ResidueSequence):

    def __init__(self, name, residues):
        self.name = name
        ResidueSequence.__init__(self, residues)
        self.alpha_helices = []


    def __repr__(self):
        return "<Chain %s>" % self.name



class BindingSite(ResiduicStructure):

    def __init__(self, residues, ligand=None):
        self.ligand = ligand
        ResiduicStructure.__init__(self, residues)


    def __repr__(self):
        return "<BindingSite (%i residues)>" % len(self.residues)



class AlphaHelix(ResidueSequence):

    def __init__(self, residues, chain):
        for residue in residues:
            assert (residue in chain.residues)
        self.chain = chain
        chain.alpha_helices.append(self)
        ResidueSequence.__init__(self, residues)


    def __repr__(self):
        return "<AlphaHelix (%i residues)>" % len(self.residues)
