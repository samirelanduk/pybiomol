import unittest
import sys
sys.path.append(".")
import pybiomol
import datetime

class TitleSectionTest(unittest.TestCase):

    def setUp(self):
        with open("tests/pdb/pdb_files/title_data.pdb") as f:
            pdb_file = pybiomol.PdbFile(f.read())
            self.data_file = pybiomol.PdbDataFile(pdb_file)


    def test_can_make_datafile(self):
        self.assertRegex(str(self.data_file), r"<[\S]{4} PdbDataFile>")


    def test_header(self):
        self.assertEqual(self.data_file.classification, "LYASE")
        self.assertEqual(
         self.data_file.deposition_date, datetime.datetime(2002, 5, 6).date()
        )
        self.assertEqual(self.data_file.pdb_code, "1LOL")


    def test_obslte(self):
        self.assertTrue(self.data_file.is_obsolete)
        self.assertEqual(
         self.data_file.obsolete_date,
         datetime.datetime(1994, 1, 31).date()
        )
        self.assertEqual(
         self.data_file.replacement_code,
         "2MBP"
        )


    def test_title(self):
        self.assertEqual(
         self.data_file.title,
         "CRYSTAL STRUCTURE OF OROTIDINE MONOPHOSPHATE DECARBOXYLASE COMPLEX WITH XMP"
        )


    def test_split(self):
        self.assertEqual(
         self.data_file.split_codes,
         [
          "1VOQ", "1VOR", "1VOS", "1VOU", "1VOV", "1VOW",
          "1VOX", "1VOY", "1VP0", "1VOZ", "1VOY", "1VP0",
          "1VOZ", "1VOZ", "1VOQ", "1VOR", "1VOS", "1VOU",
          "1VOV", "1VOW", "1VOX", "1VOY", "1VP0", "1VOZ"
         ]
        )



if __name__ == "__main__":
    unittest.main()
