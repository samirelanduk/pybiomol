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
           "content": "SEQUENCE\n"
            "AUTHOR STATES THAT ALTHOUGH RESIDUES 1 AND 1001 ARE MET\n"
            "AND RESIDUES 101 AND 1101 ARE ARG ACCORDING TO THE\n"
            "SWISSPROT ENTRY, RESIDUES 1 AND 1001 WERE LEU AND RESIDUES\n"
            "101 AND 1101 WERE PRO IN THE ORIGINAL CONSTRUCT CLONED\n"
            "OF MT GENOMIC DNA."
          }
         ]
        )
        self.assertEqual(self.empty_data_file.remarks, [])



if __name__ == "__main__":
    unittest.main()
