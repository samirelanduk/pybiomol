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



if __name__ == "__main__":
    unittest.main()
