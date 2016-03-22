class PdbFile:

    def __init__(self, file_contents):
        self.file_contents = "".join([
         char for char in file_contents if 32 <= ord(char) <= 126 or char=="\n"
        ])



class PdbRecord:

    def __init__(self, number, line):
        self.number = number
        self.text = line.ljust(80)
        self.name = self.text[:6].strip()
        self.contents = self.text[6:]


    def __repr__(self):
        return "<%s Record>" % self.name


    def __getitem__(self, key):
        return self.text[key]
