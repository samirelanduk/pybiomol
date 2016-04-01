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


    def __repr__(self):
        return "<%s PdbDataFile>" % self.pdb_code if self.pdb_code else "????"


    def merge_records(self, records, start, join=" ", dont_condense=""):
        string = join.join([r[start:] for r in records])
        condense = [char for char in " ;:," if char not in dont_condense]
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
        self.classification = header[10:50].strip() if header else None
        self.deposition_date = datetime.datetime.strptime(
         header[50:59], "%d-%b-%y"
        ).date() if header else None
        self.pdb_code = header[62:66].strip() if header else None


    def process_obslte(self):
        obslte = self.pdb_file.get_record_by_name("OBSLTE")
        self.is_obsolete = bool(obslte)
        self.obsolete_date = datetime.datetime.strptime(
         obslte[11:20], "%d-%b-%y"
        ).date() if obslte else None
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
