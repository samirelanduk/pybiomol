import unittest
import sys
sys.path.append(".")
import pybiomol
import datetime

class PdbTest(unittest.TestCase):

    def setUp(self):
        self.pdb = pybiomol.get_pdb_from_file("tests/pdb/pdb_files/1SAM.pdb")



class PdbInformationTest(PdbTest):

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



class PdbLigandClassTest(PdbTest):

    def test_can_create_ligand_classes(self):
        self.assertEqual(
         len(self.pdb.small_molecule_types),
         1
        )
        self.assertIsInstance(
         self.pdb.small_molecule_types[0],
         type
        )


    def test_ligand_class_structure(self):
        self.assertEqual(
         self.pdb.small_molecule_types[0].het_code,
         "BU2"
        )
        self.assertEqual(
         self.pdb.small_molecule_types[0].het_name,
         "1,3-BUTANEDIOL"
        )
        self.assertEqual(
         self.pdb.small_molecule_types[0].het_formula,
         "2(C4 H10 O2)"
        )
        self.assertEqual(
         self.pdb.small_molecule_types[0].synonyms,
         ["BUTYL-BUTYL-BUTYL-BUTALOL"]
        )
        self.assertFalse(self.pdb.small_molecule_types[0].is_water)





class PdbModelTest(PdbTest):

    def check_atom_bonds_other_atoms(self, atom_id, other_atom_ids):
        for other_atom_id in other_atom_ids:
            self.assertIn(
             self.pdb.model.get_atom_by_id(other_atom_id),
             self.pdb.model.get_atom_by_id(atom_id).get_covalently_bonded_atoms()
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


    def test_pdb_can_bond_standard_atoms(self):
        self.check_atom_bonds_other_atoms(474, [475])
        self.check_atom_bonds_other_atoms(475, [474, 478, 476])
        self.check_atom_bonds_other_atoms(476, [475, 477])
        self.check_atom_bonds_other_atoms(478, [475, 479])
        self.check_atom_bonds_other_atoms(479, [478, 480, 481])


    def test_pdb_can_link_residues(self):
        self.check_atom_bonds_other_atoms(476, [482])
        self.check_atom_bonds_other_atoms(484, [493])


    def test_pdb_can_process_ligands(self):
        self.assertEqual(len(self.pdb.model.small_molecules), 2)
        for ligand in self.pdb.model.small_molecules:
            self.assertIsInstance(ligand, pybiomol.PdbSmallMolecule)
            self.assertIsInstance(ligand, self.pdb.small_molecule_types[0])
            str(ligand)
            for atom in ligand.atoms:
                self.assertEqual(atom.molecule, ligand)


    def test_pdb_can_process_residues(self):
        self.assertEqual(len(self.pdb.model.residues), 6)
        for residue in self.pdb.model.residues:
            self.assertIsInstance(residue, pybiomol.PdbResidue)
            self.assertIsInstance(residue, pybiomol.Residue)
            self.assertIsInstance(residue.name, str)
            self.assertIsInstance(residue.residue_id, int)
            for atom in residue.atoms:
                self.assertEqual(atom.residue, residue)




if __name__ == "__main__":
    unittest.main()
