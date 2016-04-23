import unittest
import sys
sys.path.append(".")
import pybiomol
from test_chemstructure import ChemTest

class MacroTest(ChemTest):

    def get_residue(self):
        atoms = [self.get_atom() for _ in range(10)]
        for index, atom in enumerate(atoms[:-1]):
            atom.covalent_bond_to(atoms[index+1])
        residue = pybiomol.Residue("VAL", atoms)
        return residue


class ResidueTest(MacroTest):

    def test_can_make_resiude(self):
        residue = self.get_residue()
        str(residue)



class ResiduicStructureTest(MacroTest):

    def test_can_make_residuic_structure(self):
        residues = [self.get_residue() for _ in range(10)]
        residuic_structure = pybiomol.ResiduicStructure(residues)
        str(residuic_structure)


if __name__ == "__main__":
    unittest.main()
