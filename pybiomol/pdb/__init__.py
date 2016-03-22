import requests
from .file import *
from .exceptions import *

def get_pdb_from_file(path):
    with open(path) as f:
        pdb_file = PdbFile(f.read())
    return pdb_file


def get_pdb_remotely(code):
    response = requests.get(
     "http://www.rcsb.org/pdb/files/%s.pdb" % code
    )
    if response.status_code == 200 and response.text[:6] == "HEADER":
        contents = response.text
    else:
        raise InvalidPdbCode(
         "%s does not seem to be a valid PDB code." % code
        )

    pdb_file = PdbFile(contents)
    return pdb_file
