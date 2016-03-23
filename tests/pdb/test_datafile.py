import unittest
import sys
sys.path.append(".")
import pybiomol
import datetime

class TitleSectionTest(unittest.TestCase):

    def setUp(self):
        with open("tests/pdb/title_data.pdb") as f:
            pdb_file = pybiomol.PdbFile(f.read())
            self.data_file = pybiomol.PdbDataFile(pdb_file)


    def test_can_make_datafile(self):
        self.assertRegex(str(self.data_file), r"<[\S]{4} PdbDataFile>")


    def test_header(self):
        self.assertEqual(self.data_file.classification, "LYASE")
        self.assertEqual(
         self.data_file.deposition_date, datetime.datetime(2006, 5, 2).date()
        )
        self.assertEqual(self.data_file.pdb_code, "1LOL")



if __name__ == "__main__":
    unittest.main()
