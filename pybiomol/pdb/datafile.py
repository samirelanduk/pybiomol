import datetime

class PdbDataFile:

    def __init__(self, pdb_file):
        self.pdb_file = pdb_file

        self.process_header()
        self.process_obslte()
        self.process_title()
        self.process_split()
        self.process_caveat()
        self.process_compnd()
        self.process_source()
        self.process_keywds()
        self.process_expdta()
        self.process_nummdl()
        self.process_mdltyp()
        self.process_author()
        self.process_revdat()
        self.process_sprsde()
        self.process_jrnl()
        self.process_remark()

        self.process_dbref()
        self.process_seqadv()
        self.process_seqres()
        self.process_modres()

        self.process_het()
        self.process_hetnam()
        self.process_hetsyn()
        self.process_formul()

        self.process_helix()

    def __repr__(self):
        return "<%s PdbDataFile>" % self.pdb_code if self.pdb_code else "????"


    def date_from_string(self, s):
        return datetime.datetime.strptime(
         s, "%d-%b-%y"
        ).date()


    def merge_records(self, records, start, join=" ", dont_condense=""):
        string = join.join([r.text[start:].rstrip() if r.text[start:].rstrip() else "" for r in records])
        condense = [char for char in " ;:,-" if char not in dont_condense]
        for char in condense:
            string = string.replace(char + " ", char)
        return string


    def records_to_token_value_dicts(self, records):
        string = self.merge_records(records, 10)
        pairs = string.split(";")
        pairs = [pair.split(":") for pair in pairs if pair]
        entities = []
        entity = {}
        for pair in pairs:
            if pair[1] == "NO":
                pair[1] = False
            elif pair[1] == "YES":
                pair[1] = True
            elif pair[1].isnumeric():
                pair[1] = int(pair[1])
            elif pair[0] == "CHAIN" or pair[0] == "SYNONYM":
                pair[1] = pair[1].replace(", ", ",").split(",")
            if pair[0] == "MOL_ID":
                if entity: entities.append(entity)
                entity = {}
            entity[pair[0]] = pair[1]
        if entity: entities.append(entity)
        return entities


    def process_header(self):
        header = self.pdb_file.get_record_by_name("HEADER")
        self.classification = header[10:50] if header else None
        self.deposition_date = self.date_from_string(header[50:59]) if header else None
        self.pdb_code = header[62:66].strip() if header else None


    def process_obslte(self):
        obslte = self.pdb_file.get_record_by_name("OBSLTE")
        self.is_obsolete = bool(obslte)
        self.obsolete_date = self.date_from_string(obslte[11:20]) if obslte else None
        self.replacement_code = obslte[31:35] if obslte else None


    def process_title(self):
        titles = self.pdb_file.get_records_by_name("TITLE")
        title = self.merge_records(titles, 10)
        self.title = title if title else None


    def process_split(self):
        splits = self.pdb_file.get_records_by_name("SPLIT")
        self.split_codes = " ".join([r[10:].strip() for r in splits]).split()


    def process_caveat(self):
        caveats = self.pdb_file.get_records_by_name("CAVEAT")
        caveat = self.merge_records(caveats, 19)
        self.caveat = caveat if caveat else None


    def process_compnd(self):
        records = self.pdb_file.get_records_by_name("COMPND")
        self.compounds = self.records_to_token_value_dicts(records)


    def process_source(self):
        records = self.pdb_file.get_records_by_name("SOURCE")
        self.sources = self.records_to_token_value_dicts(records)


    def process_keywds(self):
        keywords = self.pdb_file.get_records_by_name("KEYWDS")
        keyword_text = self.merge_records(keywords, 10)
        self.keywords = keyword_text.split(",") if keyword_text else []


    def process_expdta(self):
        expdta = self.pdb_file.get_records_by_name("EXPDTA")
        expdta_text = self.merge_records(expdta, 10)
        self.experimental_techniques = expdta_text.split(";") if expdta_text else []


    def process_nummdl(self):
        nummdl = self.pdb_file.get_record_by_name("NUMMDL")
        self.model_num = int(nummdl[10:14]) if nummdl and nummdl[10:14] else 1


    def process_mdltyp(self):
        mdltyps = self.pdb_file.get_records_by_name("MDLTYP")
        mdltyp_text = self.merge_records(mdltyps, 10, dont_condense=",")
        self.model_annotations = [
         ann.strip() for ann in mdltyp_text.split(";") if ann.strip()
        ]


    def process_author(self):
        authors = self.pdb_file.get_records_by_name("AUTHOR")
        self.authors = self.merge_records(authors, 10).split(",") if authors else []


    def process_revdat(self):
        revdats = self.pdb_file.get_records_by_name("REVDAT")
        numbers = sorted(list(set([int(r[7:10]) for r in revdats])))
        self.revisions = []
        for number in numbers:
            records = [r for r in revdats if int(r[7:10]) == number]
            rec_types = self.merge_records(records, 39).split()
            self.revisions.append({
             "number": number,
             "date": self.date_from_string(records[0][13:22]),
             "type": int(records[0][31]),
             "records": [r for r in rec_types if r]
            })


    def process_sprsde(self):
        sprsde = self.pdb_file.get_record_by_name("SPRSDE")
        self.supercedes = sprsde[31:75].split() if sprsde else []
        self.supercede_date = self.date_from_string(sprsde[11:20]) if sprsde else None


    def process_jrnl(self):
        jrnls = self.pdb_file.get_records_by_name("JRNL")
        if not jrnls:
            self.journal = None
        else:
            self.journal = {}
            auths = [r for r in jrnls if r[12:16] == "AUTH"]
            self.journal["authors"] = self.merge_records(auths, 19).split(",") if auths else []
            titls = [r for r in jrnls if r[12:16] == "TITL"]
            self.journal["title"] = self.merge_records(titls, 19) if titls else None
            edits = [r for r in jrnls if r[12:16] == "EDIT"]
            self.journal["editors"] = self.merge_records(auths, 19).split(",") if edits else []
            refs = [r for r in jrnls if r[12:16] == "REF"]
            self.journal["reference"] = {}
            if refs and "TO BE PUBLISHED" in refs[0]:
                self.reference = {
                 "published": False, "publication": None,
                 "volume": None, "page": None, "year": None
                }
            elif refs:
                self.journal["reference"] = {
                 "published": True,
                 "publication": refs[0][19:47],
                 "volume": int(refs[0][51:55]),
                 "page": int(refs[0][56:61]),
                 "year": int(refs[0][62:66])
                }
            publs = [r for r in jrnls if r[12:16] == "PUBL"]
            self.journal["publisher"] = self.merge_records(publs, 19, dont_condense=",:;") if publs else None
            refns = [r for r in jrnls if r[12:16] == "REFN"]
            self.journal["reference_number"] = {
             "type": refns[0][35:39],
             "value": refns[0][40:65]
            } if refns else {}
            pmids = [r for r in jrnls if r[12:16] == "PMID"]
            self.journal["pubmed"] = pmids[0][19:79] if pmids else None
            dois = [r for r in jrnls if r[12:16] == "DOI"]
            self.journal["doi"] = dois[0][19:79] if dois else None


    def process_remark(self):
        remarks = self.pdb_file.get_records_by_name("REMARK")
        remark_numbers = sorted(list(set([int(r[7:10]) for r in remarks])))
        self.remarks = []
        for number in remark_numbers:
            recs = [r for r in remarks if int(r[7:10]) == number]
            remark = {
             "number": number,
             "content": self.merge_records(recs[1:], 11, join="\n", dont_condense=" ,:;")
            }
            self.remarks.append(remark)


    def process_dbref(self):
        dbrefs = self.pdb_file.get_records_by_name("DBREF")
        self.dbreferences = [{
         "chain": r[12],
         "sequence_begin": int(r[14:18]),
         "insert_begin": r[18],
         "sequence_end": int(r[20:24]),
         "insert_end": r[24],
         "database": r[26:32],
         "accession": r[33:40],
         "db_id": r[42:54],
         "db_sequence_begin": int(r[55:60]),
         "db_insert_begin": r[60],
         "db_sequence_end": int(r[62:67]),
         "db_insert_end": r[67]
        } for r in dbrefs]
        dbref1s = self.pdb_file.get_records_by_name("DBREF1")
        dbref2s = self.pdb_file.get_records_by_name("DBREF2")
        ref_pairs = zip(dbref1s, dbref2s)
        self.dbreferences += [{
         "chain": pair[0][12],
         "sequence_begin": int(pair[0][14:18]),
         "insert_begin": pair[0][18],
         "sequence_end": int(pair[0][20:24]),
         "insert_end": pair[0][24],
         "database": pair[0][26:32],
         "accession": pair[1][18:40],
         "db_id": pair[0][47:67],
         "db_sequence_begin": int(pair[1][45:55]),
         "db_insert_begin": None,
         "db_sequence_end": int(pair[1][57:67]),
         "db_insert_end": None
        } for pair in ref_pairs]
        self.dbreferences = sorted(self.dbreferences, key=lambda k: k["chain"])


    def process_seqadv(self):
        seqadvs = self.pdb_file.get_records_by_name("SEQADV")
        self.sequence_differences = [{
         "residue_name": r[12:15],
         "chain": r[16],
         "residue_number": int(r[18:22]) if r[18:22] else None,
         "insert_code": r[22],
         "database": r[24:28],
         "accession": r[29:38],
         "db_residue_name": r[39:42],
         "db_residue_number": int(r[43:48]) if r[43:48] else None,
         "conflict": r[49:70]
        } for r in seqadvs]


    def process_seqres(self):
        seqres = self.pdb_file.get_records_by_name("SEQRES")
        chains = sorted(list(set([r[11] for r in seqres])))
        self.residue_sequences = []
        for chain in chains:
            records = [r for r in seqres if r[11] == chain]
            self.residue_sequences.append({
             "chain": chain,
             "length": int(records[0][13:17]),
             "residues": self.merge_records(records, 19).split()
            })


    def process_modres(self):
        modres = self.pdb_file.get_records_by_name("MODRES")
        self.modifies_residues = [{
         "residue_name": r[12:15],
         "chain": r[16],
         "residue_number": int(r[18:22]),
         "insert_code": r[22],
         "standard_resisdue_name": r[24:27],
         "comment": r[29:70]
        } for r in modres]


    def process_het(self):
        hets = self.pdb_file.get_records_by_name("HET")
        self.hets = [{
         "het_id": r[7:10] if r[7:10] else None,
         "chain": r[12],
         "het_number": int(r[13:17]),
         "insert_code": r[17],
         "atom_num": int(r[20:25]),
         "description": r[30:70]
        } for r in hets]


    def process_hetnam(self):
        hetnams = self.pdb_file.get_records_by_name("HETNAM")
        ids = list(set([r[11:14] for r in hetnams]))
        self.het_names = {
         het_id: self.merge_records(
          [r for r in hetnams if r[11:14] == het_id], 15, dont_condense=":;"
         ) for het_id in ids
        }


    def process_hetsyn(self):
        hetsyns = self.pdb_file.get_records_by_name("HETSYN")
        ids = list(set([r[11:14] for r in hetsyns]))
        self.het_synonyms = {
         het_id: self.merge_records(
          [r for r in hetsyns if r[11:14] == het_id], 15
         ).split(";") for het_id in ids
        }


    def process_formul(self):
        formuls = self.pdb_file.get_records_by_name("FORMUL")
        ids = list(set([r[12:15] for r in formuls]))
        self.het_formulae = {
         het_id: {
          "component_number": int([r for r in formuls if r[12:15] == het_id][0][8:10]),
          "is_water": [r for r in formuls if r[12:15] == het_id][0][18] == "*",
          "formula": self.merge_records(
           [r for r in formuls if r[12:15] == het_id], 19
          )
         } for het_id in ids
        }


    def process_helix(self):
        helix = self.pdb_file.get_records_by_name("HELIX")
        self.helices = [{
         "helix_number": int(r[7:10]) if r[7:10] else None,
         "helix_name": r[11:14],
         "start_residue_name": r[15:18],
         "start_residue_chain": r[19],
         "start_residue_number": int(r[21:25]) if r[21:25] else None,
         "start_residue_insert": r[25],
         "end_residue_name": r[27:30],
         "end_residue_chain": r[31],
         "end_residue_number": int(r[33:37]) if r[33:37] else None,
         "end_residue_insert": r[37],
         "helix_class": int(r[38:40]) if r[38:40] else None,
         "comment": r[40:70],
         "length": int(r[71:76]) if r[71:76] else None
        } for r in helix]
