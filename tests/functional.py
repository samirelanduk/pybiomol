import unittest
import sys
sys.path.append(".")
import pybiomol

class PdbTest(unittest.TestCase):

    def test_can_get_pdb_and_manipulate(self):
        # Access a PDB file online
        pdb = pybiomol.get_pdb_remotely("1LOL")

        # Check out its basic informaion
        self.assertisInstance(pdb.title, str)
        self.assertgreater(len(pdd.model.atoms), 0)



if __name__ == "__main__":
    unittest.main()
