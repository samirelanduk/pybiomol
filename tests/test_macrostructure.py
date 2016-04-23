import unittest
import sys
sys.path.append(".")
import pybiomol
from test_chemstructure import ChemTest


class ResidueTest(ChemTest):

    def test_can_make_resiude(self):
        atoms = [self.get_atom() for _ in range(10)]
        for index, atom in enumerate(atoms[:-1]):
            atom.covalent_bond_to(atoms[index+1])
        residue = pybiomol.Residue("VAL", atoms)
        str(residue)



if __name__ == "__main__":
    unittest.main()
