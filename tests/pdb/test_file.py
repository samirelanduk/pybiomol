import unittest
import sys
sys.path.append(".")
import pybiomol
from pybiomol.pdb.file import *

class FileCreation(unittest.TestCase):

    def test_can_make_basic_pdb(self):
        with open("tests/pdb/basic.pdb") as f:
            pdb = PdbFile(f.read())


    def test_weird_characters_expelled(self):
        with open("tests/pdb/weird_chars.pdb") as f:
            contents = f.read()
            chars = len(contents)
            pdb = PdbFile(contents)
            self.assertEqual(
             len(contents) - len(pdb.file_contents),
             2
            )


    def test_can_get_by_file_name(self):
        pdb = pybiomol.get_pdb_from_file("tests/pdb/basic.pdb")


    def test_can_get_by_file_remotely(self):
        pdb = pybiomol.get_pdb_remotely("1LOL")


    def test_invalid_pdb_codes(self):
        self.assertRaises(
         pybiomol.InvalidPdbCode,
         lambda: pybiomol.get_pdb_remotely("1LOLZ")
        )


if __name__ == "__main__":
    unittest.main()
