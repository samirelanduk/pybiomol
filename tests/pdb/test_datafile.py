import unittest
import sys
sys.path.append(".")
import pybiomol

class TitleSectionTest(unittest.TestCase):

    def setUp(self):
        with open("tests/pdb/title_data.pdb") as f:
            pdb_file = pybiomol.PdbFile(f.read())
            self.data_file = pybiomol.PdbDataFile(pdb_file)


    def test_can_make_datafile(self):
        self.assertEqual(str(self.data_file), "<PdbDataFile>")



if __name__ == "__main__":
    unittest.main()
