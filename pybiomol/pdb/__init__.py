import requests
from .file import *
from .datafile import *
from .chemstructure import *
from .exceptions import *

def get_pdb_from_string(string):
    pdb_file = PdbFile(string)
    pdb_datafile = PdbDataFile(pdb_file)
    return pdb_datafile


def get_pdb_from_file(path):
    with open(path) as f:
        pdb = get_pdb_from_string(f.read())
    return pdb


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

    pdb = get_pdb_from_string(contents)
    return pdb
