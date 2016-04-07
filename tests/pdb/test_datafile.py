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
            self.empty_data_file = pybiomol.PdbDataFile(pybiomol.PdbFile(""))


    def test_can_make_datafile(self):
        self.assertRegex(str(self.data_file), r"<[\S]{4} PdbDataFile>")


    def test_header(self):
        self.assertEqual(self.data_file.classification, "LYASE")
        self.assertEqual(self.empty_data_file.classification, None)
        self.assertEqual(
         self.data_file.deposition_date, datetime.datetime(2002, 5, 6).date()
        )
        self.assertEqual(self.empty_data_file.deposition_date, None)
        self.assertEqual(self.data_file.pdb_code, "1LOL")
        self.assertEqual(self.empty_data_file.pdb_code, None)


    def test_obslte(self):
        self.assertTrue(self.data_file.is_obsolete)
        self.assertFalse(self.empty_data_file.is_obsolete)
        self.assertEqual(
         self.data_file.obsolete_date,
         datetime.datetime(1994, 1, 31).date()
        )
        self.assertEqual(self.empty_data_file.obsolete_date, None)
        self.assertEqual(
         self.data_file.replacement_code,
         "2MBP"
        )
        self.assertEqual(self.empty_data_file.replacement_code, None)


    def test_title(self):
        self.assertEqual(
         self.data_file.title,
         "CRYSTAL STRUCTURE OF OROTIDINE MONOPHOSPHATE DECARBOXYLASE COMPLEX WITH XMP"
        )
        self.assertEqual(self.empty_data_file.title, None)


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
        self.assertEqual(self.empty_data_file.split_codes, [])


    def test_caveat(self):
        self.assertEqual(
         self.data_file.caveat,
         "THE CRYSTAL TRANSFORMATION IS IN ERROR BUT IS UNCORRECTABLE AT THIS TIME"
        )
        self.assertEqual(self.empty_data_file.caveat, None)


    def test_compnd(self):
        self.assertEqual(
         self.data_file.compounds,
         [
          {
           "MOL_ID": 1,
           "MOLECULE": "COWPEA CHLOROTIC MOTTLE VIRUS",
           "CHAIN": ["A", "B", "C"],
           "MUTATION": False,
           "SYNONYM": [
            "MSTING",
            "ENDOPLASMIC RETICULUM INTERFERON STIMULATOR",
            "ERIS",
            "MEDIATOR OF IRF3 ACTIVATION",
            "MMITA",
            "TRANSMEMBRANE PROTEIN 173"
           ]
          }, {
           "MOL_ID": 2,
           "MOLECULE":  "RNA (5'-(*AP*UP*AP*U)-3')",
           "CHAIN": ["D", "F"],
           "ENGINEERED": True
          }, {
           "MOL_ID": 3,
           "MOLECULE":  "RNA (5'-(*AP*U)-3')",
           "CHAIN": ["E"],
           "ENGINEERED": True,
           "EC": "3.2.1.14,3.2.1.17"
          }
         ]
        )
        self.assertEqual(self.empty_data_file.compounds, [])


    def test_source(self):
        self.assertEqual(
         self.data_file.sources,
         [
          {
           "MOL_ID": 1,
           "ORGANISM_SCIENTIFIC": "METHANOTHERMOBACTER THERMAUTOTROPHICUS STR. DELTA H",
           "ORGANISM_TAXID": 187420,
           "STRAIN": "DELTA H",
           "EXPRESSION_SYSTEM": "ESCHERICHIA COLI",
           "EXPRESSION_SYSTEM_TAXID": 562,
           "EXPRESSION_SYSTEM_PLASMID": "PET15B"
          }
         ]
        )
        self.assertEqual(self.empty_data_file.sources, [])


    def test_keywds(self):
        self.assertEqual(
         self.data_file.keywords,
         ["LYASE",  "TRICARBOXYLIC ACID CYCLE", "MITOCHONDRION", "OXIDATIVE METABOLISM"]
        )
        self.assertEqual(self.empty_data_file.keywords, [])


    def test_expdata(self):
        self.assertEqual(
         self.data_file.experimental_techniques,
         ["NEUTRON DIFFRACTION", "X-RAY DIFFRACTION"]
        )
        self.assertEqual(self.empty_data_file.experimental_techniques, [])


    def test_nummdl(self):
        self.assertEqual(self.data_file.model_num, 20)
        self.assertEqual(self.empty_data_file.model_num, 1)


    def test_mdltyp(self):
        self.assertEqual(
         self.data_file.model_annotations,
         [
          "CA ATOMS ONLY, CHAIN A, B, C, D, E, F, G, H, I, J, K",
          "P ATOMS ONLY, CHAIN X, Y, Z"
         ]
        )
        self.assertEqual(self.empty_data_file.model_annotations, [])


    def test_author(self):
        self.assertEqual(
         self.data_file.authors,
         [
          "M.B.BERRY", "B.MEADOR", "T.BILDERBACK", "P.LIANG",
          "M.GLASER", "G.N.PHILLIPS JR.", "T.L.ST. STEVENS"
         ]
        )
        self.assertEqual(self.empty_data_file.authors, [])


    def test_revdat(self):
        self.assertEqual(
         self.data_file.revisions,
         [
          {
           "number": 1, "date": datetime.datetime(2002, 8, 7).date(),
           "type": 0, "records": []
          }, {
           "number": 2, "date": datetime.datetime(2002, 8, 14).date(),
           "type": 1, "records": ["DBREF"]
          }, {
           "number": 3, "date": datetime.datetime(2003, 4, 1).date(),
           "type": 1, "records": ["JRNL"]
          }, {
           "number": 4, "date": datetime.datetime(2009, 2, 24).date(),
           "type": 1, "records": ["VERSN", "COMPND", "EXPDTA", "CAVEAT", "SOURCE", "JRNL"]
          }
         ]
        )
        self.assertEqual(self.empty_data_file.revisions, [])


    def test_sprsde(self):
        self.assertEqual(
         self.data_file.supercedes,
         ["1LH4", "2LH4"]
        )
        self.assertEqual(self.empty_data_file.supercedes, [])
        self.assertEqual(
         self.data_file.supercede_date,
         datetime.datetime(1995, 2, 27).date()
        )
        self.assertEqual(self.empty_data_file.supercede_date, None)


    def test_jrnl(self):
        self.assertEqual(
         self.data_file.journal,
         {
          "authors": [
           "J.REN", "C.NICHOLS", "L.BIRD", "P.CHAMBERLAIN", "K.WEAVER",
           "S.SHORT", "D.I.STUART", "D.K.STAMMERS"
          ],
          "title": "CRYSTAL STRUCTURES OF INHIBITOR COMPLEXES REVEAL AN ALTERNA"
          "TE BINDING MODE IN OROTIDINE-5'-MONOPHOSPHATE DECARBOXYLASE.",
          "editors": [
           "J.REN", "C.NICHOLS", "L.BIRD", "P.CHAMBERLAIN", "K.WEAVER",
           "S.SHORT", "D.I.STUART", "D.K.STAMMERS"
          ],
          "reference": {"published": True, "publication": "SCIENCE", "volume": 282, "page": 2088, "year": 1998},
          "publisher": "AMERICAN ASSOCIATION FOR THE ADVANCEMENT OF SCIENCE WASHINGTON, D.C.",
          "reference_number": {"type": "ISSN", "value": "0036-8075"},
          "pubmed": "12011084",
          "doi": "10.1074/JBC.M202362200"
         }
        )
        self.assertEqual(self.empty_data_file.journal, None)


    def test_remark(self):
        self.maxDiff = None
        self.assertEqual(
         self.data_file.remarks,
         [
          {
           "number": 2,
           "content": "RESOLUTION.    1.90 ANGSTROMS."
          }, {
           "number": 4,
           "content": "1LOL COMPLIES WITH FORMAT V. 3.15, 01-DEC-08"
          }, {
           "number": 999,
           "content": " SEQUENCE\n"
            "AUTHOR STATES THAT ALTHOUGH RESIDUES 1 AND 1001 ARE MET\n"
            "AND RESIDUES 101 AND 1101 ARE ARG ACCORDING TO THE\n"
            "SWISSPROT ENTRY, RESIDUES 1 AND 1001 WERE LEU AND RESIDUES\n"
            "101 AND 1101 WERE PRO IN THE ORIGINAL CONSTRUCT CLONED\n"
            "OF MT GENOMIC DNA."
          }
         ]
        )
        self.assertEqual(self.empty_data_file.remarks, [])



class PrimaryStructureSectionTest(unittest.TestCase):

    def setUp(self):
        with open("tests/pdb/pdb_files/primary_structure_data.pdb") as f:
            pdb_file = pybiomol.PdbFile(f.read())
            self.data_file = pybiomol.PdbDataFile(pdb_file)
            self.empty_data_file = pybiomol.PdbDataFile(pybiomol.PdbFile(""))


    def test_dbref(self):
        self.assertEqual(
         self.data_file.dbreferences,
         [
          {
           "chain": "A",
           "sequence_begin": 1,
           "insert_begin": None,
           "sequence_end": 229,
           "insert_end": None,
           "database": "UNP",
           "accession": "O26232",
           "db_id": "PYRF_METTH",
           "db_sequence_begin": 1,
           "db_insert_begin": None,
           "db_sequence_end": 228,
           "db_insert_end": None
          }, {
           "chain": "B",
           "sequence_begin": 1001,
           "insert_begin": None,
           "sequence_end": 1229,
           "insert_end": None,
           "database": "UNP",
           "accession": "O26232",
           "db_id": "PYRF_METTH",
           "db_sequence_begin": 1,
           "db_insert_begin": None,
           "db_sequence_end": 228,
           "db_insert_end": None
          }, {
           "chain": "C",
           "sequence_begin": 61,
           "insert_begin": None,
           "sequence_end": 322,
           "insert_end": None,
           "database": "GB",
           "accession": "46197919",
           "db_id": "AE017221",
           "db_sequence_begin": 1534489,
           "db_insert_begin": None,
           "db_sequence_end": 1537377,
           "db_insert_end": None
          }
         ]
        )
        self.assertEqual(self.empty_data_file.dbreferences, [])


    def test_seqadv(self):
        self.assertEqual(
         self.data_file.sequence_differences,
         [
          {
           "residue_name": "GLU",
           "chain": "A",
           "residue_number": 229,
           "insert_code": None,
           "database": "UNP",
           "accession": "O26232",
           "db_residue_name": None,
           "db_residue_number": None,
           "conflict": "INSERTION"
          }, {
           "residue_name": "GLU",
           "chain": "B",
           "residue_number": 1229,
           "insert_code": None,
           "database": "UNP",
           "accession": "O26232",
           "db_residue_name": None,
           "db_residue_number": None,
           "conflict": "INSERTION"
          }
         ]
        )
        self.assertEqual(self.empty_data_file.sequence_differences, [])


    def test_seqres(self):
        self.assertEqual(
         self.data_file.residue_sequences,
         [
          {
           "chain": "A",
           "length": 229,
           "residues": [
            "LEU", "ARG", "SER", "ARG", "ARG", "VAL", "ASP", "VAL",
            "MET", "ASP", "VAL", "MET", "ASN", "ARG", "LEU", "CYS"
            ]
          }, {
           "chain": "B",
           "length": 229,
           "residues": [
            "LEU", "ARG", "SER", "ARG", "ARG", "VAL", "ASP", "VAL",
            "MET", "ASP", "VAL", "MET", "ASN", "ARG", "LEU", "CYS"
            ]
          }
         ]
        )
        self.assertEqual(self.empty_data_file.residue_sequences, [])


    def test_modres(self):
        self.assertEqual(
         self.data_file.modifies_residues,
         [
          {
           "residue_name": "ASN",
           "chain": "A",
           "residue_number": 74,
           "insert_code": None,
           "standard_resisdue_name": 'ASN',
           "comment": "GLYCOSYLATION SITE"
          }, {
           "residue_name": "1MG",
           "chain": "D",
           "residue_number": 1937,
           "insert_code": None,
           "standard_resisdue_name": 'G',
           "comment": "1N-METHYLGUANOSINE-5'-MONOPHOSPHATE"
          }
         ]
        )
        self.assertEqual(self.empty_data_file.modifies_residues, [])



class HeterogenSectionTest(unittest.TestCase):

    def setUp(self):
        with open("tests/pdb/pdb_files/heterogen_data.pdb") as f:
            pdb_file = pybiomol.PdbFile(f.read())
            self.data_file = pybiomol.PdbDataFile(pdb_file)
            self.empty_data_file = pybiomol.PdbDataFile(pybiomol.PdbFile(""))


    def test_het(self):
        self.assertEqual(
         self.data_file.hets,
         [
          {
           "het_id": "K",
           "chain": "A",
           "het_number": 501,
           "insert_code": None,
           "atom_num": 1,
           "description": None
          }, {
           "het_id": "K",
           "chain": "A",
           "het_number": 502,
           "insert_code": None,
           "atom_num": 1,
           "description": None
          }, {
           "het_id": "K",
           "chain": "A",
           "het_number": 503,
           "insert_code": None,
           "atom_num": 1,
           "description": None
          }, {
           "het_id": "K",
           "chain": "A",
           "het_number": 504,
           "insert_code": None,
           "atom_num": 1,
           "description": None
          }, {
           "het_id": "PIO",
           "chain": "A",
           "het_number": 400,
           "insert_code": None,
           "atom_num": 40,
           "description": None
          }
         ]
        )
        self.assertEqual(self.empty_data_file.hets, [])


    def test_hetnam(self):
        self.assertEqual(
         self.data_file.het_names,
         {
          "K": "POTASSIUM ION",
          "PIO": "(1R)-1,4-ANHYDRO-2-DEOXY-1-(6-METHYL-2,4-DIOXO-1,2,3,4-TETRAH"
          "YDROQUINAZOLIN-8-YL)-5-O-PHOSPHONO-D-ERYTHRO-PENTITOL"
         }
        )
        self.assertEqual(self.empty_data_file.het_names, {})


    def test_hetsyn(self):
        self.assertEqual(
         self.data_file.het_synonyms,
         {
          "K": ["BOOM BOOM BOMB"],
          "PIO": [
           "L-ALPHA-PHOSPHATIDYL-D-MYO-INOSITOL 4,5-DIPHOSPHATE,DIOCTANOYL",
           "L-ALPHA-PHOSPHATIDYLINOSITOL 4,5-DIPHOSPHATE SODIUM SALT",
           "PIP2",
           "1,2-DIACYL-SN-GLYCERO-3-PHOSPHO-(1-D-MYO-INOSITOL4,5-BISPHOSPHATE)",
           "TRIPHOSPHOINOSITIDE"
          ]
         }
        )
        self.assertEqual(self.empty_data_file.het_synonyms, {})


    def test_formul(self):
        self.assertEqual(
         self.data_file.het_formulae,
         {
          "K": {"component_number": 2, "is_water": False, "formula": "4(K 1+)"}
         }
        )
        self.assertEqual(self.empty_data_file.het_formulae, {})



class SecondaryStructureSectionTest(unittest.TestCase):

    def setUp(self):
        with open("tests/pdb/pdb_files/secondary_structure_data.pdb") as f:
            pdb_file = pybiomol.PdbFile(f.read())
            self.data_file = pybiomol.PdbDataFile(pdb_file)
            self.empty_data_file = pybiomol.PdbDataFile(pybiomol.PdbFile(""))


    def test_helix(self):
        self.assertEqual(
         self.data_file.helices,
         [
          {
           "helix_number": 1,
           "helix_name": "1",
           "start_residue_name": "ASP",
           "start_residue_chain": "A",
           "start_residue_number": 61,
           "start_residue_insert": None,
           "end_residue_name": "ASP",
           "end_residue_chain": "A",
           "end_residue_number": 69,
           "end_residue_insert": None,
           "helix_class": 1,
           "comment": None,
           "length": 9
          }, {
           "helix_number": 2,
           "helix_name": "2",
           "start_residue_name": "ASP",
           "start_residue_chain": "A",
           "start_residue_number": 69,
           "start_residue_insert": None,
           "end_residue_name": "VAL",
           "end_residue_chain": "A",
           "end_residue_number": 75,
           "end_residue_insert": None,
           "helix_class": 1,
           "comment": None,
           "length": 7
          }
         ]
        )
        self.assertEqual(self.empty_data_file.helices, [])


    def test_sheet(self):
        self.assertEqual(
         self.data_file.sheets,
         [
          {
           "sheet": "A",
           "strand_count": 2,
           "strands": [{
            "strand_number": 1,
            "start_residue_name": "VAL",
            "start_residue_chain": "A",
            "start_residue_number": 124,
            "start_residue_insert": None,
            "end_residue_name": "LEU",
            "end_residue_chain": "A",
            "end_residue_number": 125,
            "end_residue_insert": None,
            "sense": 0,
            "current_atom": None,
            "current_residue_name": None,
            "current_chain": None,
            "current_residue_number": None,
            "current_insert": None,
            "previous_atom": None,
            "previous_residue_name": None,
            "previous_chain": None,
            "previous_residue_number": None,
            "previous_insert": None
           }, {
            "strand_number": 2,
            "start_residue_name": "CYS",
            "start_residue_chain": "A",
            "start_residue_number": 150,
            "start_residue_insert": None,
            "end_residue_name": "VAL",
            "end_residue_chain": "A",
            "end_residue_number": 151,
            "end_residue_insert": None,
            "sense": -1,
            "current_atom": "O",
            "current_residue_name": "CYS",
            "current_chain": "A",
            "current_residue_number": 150,
            "current_insert": None,
            "previous_atom": "N",
            "previous_residue_name": "LEU",
            "previous_chain": "A",
            "previous_residue_number": 125,
            "previous_insert": None
           }]
          }
         ]
        )
        self.assertEqual(self.empty_data_file.sheets, [])



class ConnectivityAnnotationSectionTest(unittest.TestCase):

    def setUp(self):
        with open("tests/pdb/pdb_files/connectivity_annotation_data.pdb") as f:
            pdb_file = pybiomol.PdbFile(f.read())
            self.data_file = pybiomol.PdbDataFile(pdb_file)
            self.empty_data_file = pybiomol.PdbDataFile(pybiomol.PdbFile(""))


    def test_ssbond(self):
        self.assertEqual(
         self.data_file.ss_bonds,
         [{
          "serial_num": 1,
          "residue_name_1": "CYS",
          "chain_1": "A",
          "residue_number_1": 123,
          "insert_code_1": None,
          "residue_name_2": "CYS",
          "chain_2": "A",
          "residue_number_2": 155,
          "insert_code_2": None,
          "symmetry_1": "1555",
          "symmetry_2": "1555",
          "length": 2.04
         }]
        )
        self.assertEqual(self.empty_data_file.ss_bonds, [])


    def test_link(self):
        self.assertEqual(
         self.data_file.links,
         [{
          "atom_1": "O",
          "alt_loc_1": None,
          "residue_name_1": "TYR",
          "chain_1": "A",
          "residue_number_1": 146,
          "insert_code_1": None,
          "atom_2": "K",
          "alt_loc_2": None,
          "residue_name_2": "K",
          "chain_2": "A",
          "residue_number_2": 501,
          "insert_code_2": None,
          "symmetry_1": "1555",
          "symmetry_2": "1555",
          "length": 2.75
         }, {
          "atom_1": "OG1",
          "alt_loc_1": None,
          "residue_name_1": "THR",
          "chain_1": "A",
          "residue_number_1": 143,
          "insert_code_1": None,
          "atom_2": "K",
          "alt_loc_2": None,
          "residue_name_2": "K",
          "chain_2": "A",
          "residue_number_2": 504,
          "insert_code_2": None,
          "symmetry_1": "1555",
          "symmetry_2": "1555",
          "length": None
         }]
        )
        self.assertEqual(self.empty_data_file.links, [])


    def test_cispep(self):
        self.assertEqual(
         self.data_file.cis_peptides,
         [{
          "serial_num": None,
          "residue_name_1": "ASP",
          "chain_1": "B",
          "residue_number_1": 1188,
          "insert_1": None,
          "residue_name_2": "PRO",
          "chain_2": "B",
          "residue_number_2": 1189,
          "insert_2": None,
          "model_number": 0,
          "angle": 0.35
         }]
        )



class MiscellaneousSectionTest(unittest.TestCase):

    def setUp(self):
        with open("tests/pdb/pdb_files/miscellaneous_data.pdb") as f:
            pdb_file = pybiomol.PdbFile(f.read())
            self.data_file = pybiomol.PdbDataFile(pdb_file)
            self.empty_data_file = pybiomol.PdbDataFile(pybiomol.PdbFile(""))


    def test_site(self):
        self.assertEqual(
         self.data_file.sites,
         [
          {
           "site_id": "AC1",
           "residue_count": 6,
           "residues": [
            {"residue_name": "ASP", "chain": "A", "residue_number": 70, "insert_code": None},
            {"residue_name": "LYS", "chain": "A", "residue_number": 72, "insert_code": None},
            {"residue_name": "HOH", "chain": "A", "residue_number": 3015, "insert_code": None}
           ]
          }, {
           "site_id": "AC3",
           "residue_count": 18,
           "residues": [
            {"residue_name": "ALA", "chain": "A", "residue_number": 18, "insert_code": None},
            {"residue_name": "ASP", "chain": "A", "residue_number": 20, "insert_code": None},
            {"residue_name": "LYS", "chain": "A", "residue_number": 42, "insert_code": None},
            {"residue_name": "ASP", "chain": "A", "residue_number": 70, "insert_code": None},
            {"residue_name": "MET", "chain": "A", "residue_number": 126, "insert_code": None},
            {"residue_name": "SER", "chain": "A", "residue_number": 127, "insert_code": None},
            {"residue_name": "SER", "chain": "A", "residue_number": 158, "insert_code": None},
            {"residue_name": "PRO", "chain": "A", "residue_number": 180, "insert_code": None}
           ]
          }
         ]
        )
        self.assertEqual(self.empty_data_file.sites, [])



class CrystalSectionTest(unittest.TestCase):

    def setUp(self):
        with open("tests/pdb/pdb_files/crystal_data.pdb") as f:
            pdb_file = pybiomol.PdbFile(f.read())
            self.data_file = pybiomol.PdbDataFile(pdb_file)
            self.empty_data_file = pybiomol.PdbDataFile(pybiomol.PdbFile(""))


    def test_crystal(self):
        self.assertEqual(self.data_file.crystal_a, 57.57)
        self.assertEqual(self.data_file.crystal_b, 55.482)
        self.assertEqual(self.data_file.crystal_c, 66.129)
        self.assertEqual(self.data_file.crystal_alpha, 90.0)
        self.assertEqual(self.data_file.crystal_beta, 94.28)
        self.assertEqual(self.data_file.crystal_gamma, 90.0)
        self.assertEqual(self.data_file.crystal_s_group, "P 1 21 1")
        self.assertEqual(self.data_file.crystal_z, 4)
        self.assertEqual(self.empty_data_file.crystal_a, None)
        self.assertEqual(self.empty_data_file.crystal_b, None)
        self.assertEqual(self.empty_data_file.crystal_c, None)
        self.assertEqual(self.empty_data_file.crystal_alpha, None)
        self.assertEqual(self.empty_data_file.crystal_beta, None)
        self.assertEqual(self.empty_data_file.crystal_gamma, None)
        self.assertEqual(self.empty_data_file.crystal_s_group, None)
        self.assertEqual(self.empty_data_file.crystal_z, None)



if __name__ == "__main__":
    unittest.main()
