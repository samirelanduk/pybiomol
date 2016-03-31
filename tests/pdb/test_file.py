import unittest
import sys
sys.path.append(".")
import pybiomol
from pybiomol.pdb.file import *

class FileCreation(unittest.TestCase):

    def test_can_make_basic_pdb(self):
        with open("tests/pdb/pdb_files/basic.pdb") as f:
            pdb = PdbFile(f.read())


    def test_weird_characters_expelled(self):
        with open("tests/pdb/pdb_files/weird_chars.pdb") as f:
            contents = f.read()
            chars = len(contents)
            pdb = PdbFile(contents)
            self.assertEqual(
             len(contents) - len(pdb.file_contents),
             2
            )


    def test_can_get_by_file_name(self):
        pdb = pybiomol.get_pdb_from_file("tests/pdb/pdb_files/basic.pdb")


    def test_has_records(self):
        with open("tests/pdb/pdb_files/basic.pdb") as f:
            pdb = PdbFile(f.read())
            self.assertIsInstance(pdb.records, list)
            self.assertEqual(len(pdb.records), 9)
            for record in pdb.records:
                self.assertIsInstance(record, PdbRecord)


    def test_file_repr(self):
        with open("tests/pdb/pdb_files/basic.pdb") as f:
            pdb = PdbFile(f.read())
            self.assertEqual(
             str(pdb),
             "<PdbFile (9 Records)>"
            )


    def test_index_access(self):
        with open("tests/pdb/pdb_files/basic.pdb") as f:
            pdb = PdbFile(f.read())
            record = pdb[0]
            self.assertIsInstance(record, PdbRecord)
            self.assertEqual(record.name, "HEADER")


    def test_record_access(self):
        with open("tests/pdb/pdb_files/basic.pdb") as f:
            pdb = PdbFile(f.read())
            records = pdb.get_records_by_name("COMPND")
            self.assertIsInstance(records, list)
            self.assertEqual(len(records), 6)
            for record in records:
                self.assertIsInstance(record, PdbRecord)


    def test_can_get_by_file_remotely(self):
        pdb = pybiomol.get_pdb_remotely("1LOL")


    def test_invalid_pdb_codes(self):
        self.assertRaises(
         pybiomol.InvalidPdbCode,
         lambda: pybiomol.get_pdb_remotely("1LOLZ")
        )



class RecordTests(unittest.TestCase):

    def test_create_record(self):
        record = PdbRecord(45, "TEST   123  123")
        self.assertEqual(len(record.text), 80)
        self.assertEqual(record.name, "TEST")
        self.assertEqual(record.number, 45)
        self.assertTrue(record.contents.startswith(" 123  123"))
        self.assertEqual(len(record.contents), 74)


    def test_record_repr(self):
        record = PdbRecord(45, "TEST   123  123")
        self.assertEqual(
         str(record),
         "<TEST Record>"
        )


    def test_index_access(self):
        record = PdbRecord(45, "TEST   123  123")
        self.assertEqual(record[0], "T")
        self.assertEqual(record[70], None)
        self.assertEqual(record[7:10], "123")
        self.assertEqual(record[6:11], "123")
        self.assertEqual(record[4:7], None)


if __name__ == "__main__":
    unittest.main()
