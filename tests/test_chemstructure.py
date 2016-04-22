import unittest
import sys
sys.path.append(".")
import pybiomol

class ChemTest(unittest.TestCase):

    def get_atom(self, element="C", xyz=(10, 10, 10), name=None):
        atom = pybiomol.Atom(element, 1, *xyz, name=name)
        return atom



class AtomTest(ChemTest):

    def test_can_make_atom(self):
        atom = self.get_atom()
        self.assertIsInstance(atom, pybiomol.Atom)
        self.assertIsInstance(atom.element, str)
        self.assertIsInstance(atom.atom_id, int)
        self.assertIsInstance(atom.x, float)
        self.assertIsInstance(atom.y, float)
        self.assertIsInstance(atom.z, float)
        self.assertIsInstance(atom.name, str)
        self.assertEqual(atom.name, atom.element)
        str(atom)


    def test_can_make_atom_with_name(self):
        atom = self.get_atom(name="AT1")
        self.assertEqual(atom.name, "AT1")


    def test_can_get_distance_between_atoms(self):
        atom1 = self.get_atom(xyz=(-0.791, 64.789, 30.59)) # Atom 2621 in 1LOL
        atom2 = self.get_atom(xyz=(5.132, 63.307, 56.785)) # Atom 1011 in 1LOL
        pymol_calculated_distance = 26.9
        self.assertAlmostEqual(
         atom1.distance_to(atom2),
         pymol_calculated_distance,
         delta=0.01
        )


    def test_can_get_mass(self):
        atom = self.get_atom()
        self.assertAlmostEqual(atom.get_mass(), 12, delta=0.5)
        atom = self.get_atom(element="Ba")
        self.assertAlmostEqual(atom.get_mass(), 137, delta=0.5)
        atom = self.get_atom(element="XXX")
        self.assertEqual(atom.get_mass(), 0)



class AtomicStructureTest(ChemTest):

    def test_can_make_atomic_structure(self):
        atom1 = self.get_atom()
        atom2 = self.get_atom(element="N", xyz=(20, 20, 20))
        atomic_structure = pybiomol.AtomicStructure(atom1, atom2)
        self.assertIsInstance(atomic_structure, pybiomol.AtomicStructure)
        self.assertIsInstance(atomic_structure.atoms, list)
        for atom in atomic_structure.atoms:
            self.assertIsInstance(atom, pybiomol.Atom)
            self.assertIn(atom, (atom1, atom2))
        str(atomic_structure)


    def test_can_get_mass(self):
        atom1 = self.get_atom()
        atom2 = self.get_atom(element="N", xyz=(20, 20, 20))
        atomic_structure = pybiomol.AtomicStructure(atom1, atom2)
        self.assertEqual(
         atomic_structure.get_mass(),
         atom1.get_mass() + atom2.get_mass()
        )


    def test_atomic_structure_will_only_accept_atoms(self):
        self.assertRaises(
         AssertionError,
         lambda: pybiomol.AtomicStructure(self.get_atom(), "a string")
        )



class BondTest(ChemTest):

    def test_can_make_bond(self):
        atom1 = self.get_atom()
        atom2 = self.get_atom(element="N", xyz=(20, 20, 20))
        bond = pybiomol.Bond(atom1, atom2)
        self.assertIsInstance(bond, pybiomol.Bond)
        self.assertIsInstance(bond.atoms, set)
        self.assertEqual(len(bond.atoms), 2)
        for atom in bond.atoms:
            self.assertIsInstance(atom, pybiomol.Atom)
            self.assertIn(atom, (atom1, atom2))
        str(bond)


if __name__ == "__main__":
    unittest.main()