import unittest
import sys
sys.path.append(".")
import pybiomol

class AtomTest(unittest.TestCase):

    def get_atom(self, xyz=(10, 10, 10), name=None):
        atom = pybiomol.Atom("C", 1, *xyz, name=name)
        return atom


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



if __name__ == "__main__":
    unittest.main()
