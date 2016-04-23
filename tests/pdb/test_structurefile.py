import unittest
import sys
sys.path.append(".")
import pybiomol

class PdbInformationTest(unittest.TestCase):

    def setUp(self):
        self.pdb = pybiomol.get_pdb_from_file("tests/pdb/pdb_files/1SAM.pdb")


    def test_can_make_pdb(self):
        self.assertIsInstance(self.pdb, pybiomol.Pdb)
        self.assertIsInstance(self.pdb.data_file, pybiomol.PdbDataFile)
        str(self.pdb)




if __name__ == "__main__":
    unittest.main()
