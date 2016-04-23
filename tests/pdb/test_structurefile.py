import unittest
import sys
sys.path.append(".")
import pybiomol
import datetime

class PdbInformationTest(unittest.TestCase):

    def setUp(self):
        self.pdb = pybiomol.get_pdb_from_file("tests/pdb/pdb_files/1SAM.pdb")


    def test_can_make_pdb(self):
        self.assertIsInstance(self.pdb, pybiomol.Pdb)
        self.assertIsInstance(self.pdb.data_file, pybiomol.PdbDataFile)
        str(self.pdb)


    def test_title_information(self):
        self.assertEqual(self.pdb.classification, "PHOTOSYNTHESIS")
        self.assertEqual(
         self.pdb.deposition_date,
         datetime.datetime(2016, 4, 23).date()
        )
        self.assertEqual(self.pdb.pdb_code, "1SAM")
        self.assertFalse(self.pdb.is_obsolete)
        self.assertIs(self.pdb.obsolete_date, None)
        self.assertIs(self.pdb.replacement_code, None)
        self.assertEqual(
         self.pdb.title,
         "BASICALLY JUST A TEST PDB FILE THAT I HAVE CREATED FOR THE PURPOSES OF TESTING"
        )




if __name__ == "__main__":
    unittest.main()
