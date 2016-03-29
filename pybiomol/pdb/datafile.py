import datetime

class PdbDataFile:

    def __init__(self, pdb_file):
        self.pdb_file = pdb_file

        self.process_header()
        self.process_obslte()
        self.process_title()
        self.process_split()
        self.process_caveat()


    def __repr__(self):
        return "<%s PdbDataFile>" % self.pdb_code if self.pdb_code else "????"


    def merge_records(self, records, start, join=" "):
        return join.join([r[start:].strip() for r in records])


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
