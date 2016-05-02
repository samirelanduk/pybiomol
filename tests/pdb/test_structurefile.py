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
        self.assertEqual(self.pdb.split_codes, [])
        self.assertEqual(
         self.pdb.caveat,
         "THIS IS NOT A REAL PDB FILE!"
        )
        self.assertEqual(
         self.pdb.keywords,
         ["TEST", "NOT REAL", "TREADMILLISM", "CATASTROPHIC SYSTEM FAILURE"]
        )
        self.assertEqual(
         self.pdb.experimental_techniques,
         ["HAND TYPING", "PURE IMAGINATION"]
        )
        self.assertEqual(self.pdb.model_num, 2)
        self.assertEqual(self.pdb.model_annotations, [])
        self.assertEqual(
         self.pdb.authors,
         ["SAM IRELAND", "MARVIN GOODWRIGHT"]
        )
        self.assertEqual(self.pdb.revisions, [])
        self.assertEqual(self.pdb.supercedes, ["0SAM"])
        self.assertEqual(
         self.pdb.supercede_date,
         datetime.datetime(2009, 5, 23).date()
        )
        self.assertEqual(
         self.pdb.journal,
         {
          "authors": ["S. IRELAND", "M. GOODWRIGHT"],
          "title": "ADVENTURES IN MAKING UP PDB FILES.",
          "editors": ["R. STARK", "J. SNOW", "S. STARK", "C. LANNISTER"],
          "reference": {
           "published": True,
           "publication": "SPLENDID SCIENCE",
           "volume": 1,
           "page": 1,
           "year": 2016
          },
          "publisher": "FABRICATORS OF PDB DATA INC.",
          "reference_number": {"type": "ISSN", "value": "XXXX-XXXX"},
          "pubmed": "00000001",
          "doi": "XX.XXX/XXX.XXXXXXXXX"
         }
        )



class PdbModelTest(unittest.TestCase):

    def setUp(self):
        self.pdb = pybiomol.get_pdb_from_file("tests/pdb/pdb_files/1SAM.pdb")


    def check_atom_bonds_other_atoms(self, atom_id, other_atom_ids):
        self.assertEqual(
         self.pdb.model.get_atom_by_id(atom_id).get_covalently_bonded_atoms(),
         [self.pdb.model.get_atom_by_id(other_atom_id)
          for other_atom_id in other_atom_ids]
        )


    def test_pdb_has_two_models(self):
        self.assertEqual(
         len(self.pdb.models),
         2
        )
        for model in self.pdb.models:
            self.assertIsInstance(model, pybiomol.PdbModel)
            self.assertIsInstance(model, pybiomol.AtomicStructure)
        self.assertIs(self.pdb.model, self.pdb.models[0])
        str(self.pdb.model)


    def test_pdb_can_process_atoms(self):
        self.assertEqual(len(self.pdb.model.macro_atoms), 56)
        self.assertEqual(len(self.pdb.model.hetero_atoms), 12)
        self.assertEqual(len(self.pdb.model.atoms), 68)
        for atom in self.pdb.model.atoms:
            self.assertIsInstance(atom, pybiomol.PdbAtom)
            self.assertIs(atom.u11, None)
        str(atom)


    def test_pdb_can_bond_het_atoms(self):
        self.check_atom_bonds_other_atoms(3194, [3195, 3196])
        self.check_atom_bonds_other_atoms(3195, [3194])
        self.check_atom_bonds_other_atoms(3196, [3194, 3197])
        self.check_atom_bonds_other_atoms(3197, [3196, 3198, 3199])
        self.check_atom_bonds_other_atoms(3198, [3197])
        self.check_atom_bonds_other_atoms(3199, [3197])
        self.check_atom_bonds_other_atoms(3224, [3225, 3226])
        self.check_atom_bonds_other_atoms(3225, [3224])
        self.check_atom_bonds_other_atoms(3226, [3224, 3227])
        self.check_atom_bonds_other_atoms(3227, [3226, 3228, 3229])
        self.check_atom_bonds_other_atoms(3228, [3227])
        self.check_atom_bonds_other_atoms(3229, [3227])




if __name__ == "__main__":
    unittest.main()
