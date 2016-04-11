class PdbFile:

    def __init__(self, file_contents):
        self.file_contents = "".join([
         char for char in file_contents if 32 <= ord(char) <= 126 or char=="\n"
        ])
        self.records = [
         PdbRecord(i, line) for i, line in
          enumerate(self.file_contents.split("\n"), start=1) if line
        ]


    def __repr__(self):
        return "<PdbFile (%i Records)>" % len(self.records)


    def __getitem__(self, key):
        return self.records[key]


    def get_record_by_name(self, record_name):
        for record in self.records:
            if record.name.upper() == record_name.upper():
                return record


    def get_records_by_name(self, record_name):
        return [
         r for r in self.records if r.name.upper() == record_name.upper()
        ]



class PdbRecord:

    def __init__(self, number, line):
        self.number = number
        self.text = line.ljust(80)
        self.name = self.text[:6].strip()
        self.contents = self.text[6:]


    def __repr__(self):
        return "<%s Record>" % self.name


    def __getitem__(self, key):
        return self.text[key].strip() if self.text[key].strip() else None
