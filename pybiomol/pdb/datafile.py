import datetime

class PdbDataFile:

    def __init__(self, pdb_file):
        self.pdb_file = pdb_file

        self.process_header()
        self.process_obslte()


    def __repr__(self):
        return "<%s PdbDataFile>" % self.pdb_code if self.pdb_code else "????"


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
