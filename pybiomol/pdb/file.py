class PdbFile:

    def __init__(self, file_contents):
        self.file_contents = "".join([
         char for char in file_contents if 32 <= ord(char) <= 126 or char=="\n"
        ])
