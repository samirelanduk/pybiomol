import math

class Atom:

    def __init__(self, element, atom_id, x, y, z, name=None):
        self.element = element.title()
        self.atom_id = atom_id
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.name = name if name else element
        self.covalent_bonds = []


    def __repr__(self):
        return "<%s Atom>" % self.element


    def distance_to(self, other_object):
        x_sum = math.pow((other_object.x - self.x), 2)
        y_sum = math.pow((other_object.y - self.y), 2)
        z_sum = math.pow((other_object.z - self.z), 2)
        distance = math.sqrt(x_sum + y_sum + z_sum)
        return distance


    def get_mass(self):
        return PERIODIC_TABLE.get(self.element.upper(), 0)


    def covalent_bond_to(self, other_atom):
        assert isinstance(other_atom, Atom), "Can only bond atoms to other atoms, not %s" % type(other_atom)
        bond = CovalentBond(self, other_atom)
        if other_atom not in self.get_covalently_bonded_atoms():
            self.covalent_bonds.append(bond)
        if self not in other_atom.get_covalently_bonded_atoms():
            other_atom.covalent_bonds.append(bond)


    def get_covalently_bonded_atoms(self):
        atoms = []
        for bond in self.covalent_bonds:
            for atom in bond.atoms:
                if atom is not self and atom not in atoms:
                    atoms.append(atom)
        return atoms


    def get_covalently_accessible_atoms(self, already_checked=None):
        already_checked = [] if already_checked is None else already_checked
        if self not in already_checked:
            already_checked.append(self)
        i = 0
        while len([a for a in self.get_covalently_bonded_atoms() if a not in already_checked]) > 0:
            picked = [a for a in self.get_covalently_bonded_atoms() if a not in already_checked][0]
            picked.get_covalently_accessible_atoms(already_checked)
            i += 1
            if i > 10: break
        return [a for a in already_checked if a is not self]







class AtomicStructure:

    def __init__(self, *atoms):
        for atom in atoms:
            assert isinstance(atom, Atom), "AtomicStructure needs atoms, not %s" % type(atom)
        self.atoms = list(atoms)


    def __repr__(self):
        return "<Atomic Structure (%i atoms)>" % len(self.atoms)


    def get_mass(self):
        return sum([atom.get_mass() for atom in self.atoms])


class Molecule(AtomicStructure):

    def __init__(self, *atoms):
        assert set(atoms[1:]).issubset(
         set(atoms[0].get_covalently_accessible_atoms())
        ), "You can only make a molecule with atoms that are bonded to each other"
        AtomicStructure.__init__(self, *atoms)


class Bond:

    def __init__(self, atom1, atom2):
        self.atoms = set((atom1, atom2))


    def __repr__(self):
        atoms = list(self.atoms)
        return "<Bond between %s atom and %s atom>" % (atoms[0].element, atoms[1].element)


    def get_length(self):
        atoms = list(self.atoms)
        return atoms[0].distance_to(atoms[1])



class CovalentBond(Bond):
    pass



PERIODIC_TABLE = {
 "H": 1.0079, "HE": 4.0026, "LI": 6.941, "BE": 9.0122, "B": 10.811, "C": 12.0107,
  "N": 14.0067, "O": 15.9994, "F": 18.9984, "NE": 20.1797, "NA": 22.9897, "MG": 24.305,
   "AL": 26.9815, "SI": 28.0855, "P": 30.9738, "S": 32.065, "CL": 35.453, "K": 39.0983,
    "AR": 39.948, "CA": 40.078, "SC": 44.9559, "TI": 47.867, "V": 50.9415, "CR": 51.9961,
     "MN": 54.938, "FE": 55.845, "NI": 58.6934, "CO": 58.9332, "CU": 63.546, "ZN": 65.39,
      "GA": 69.723, "GE": 72.64, "AS": 74.9216, "SE": 78.96, "BR": 79.904, "KR": 83.8,
       "RB": 85.4678, "SR": 87.62, "Y": 88.9059, "ZR": 91.224, "NB": 92.9064, "MO": 95.94,
        "TC": 98, "RU": 101.07, "RH": 102.9055, "PD": 106.42, "AG": 107.8682, "CD": 112.411,
         "IN": 114.818, "SN": 118.71, "SB": 121.76, "I": 126.9045, "TE": 127.6,
          "XE": 131.293, "CS": 132.9055, "BA": 137.327, "LA": 138.9055, "CE": 140.116,
           "PR": 140.9077, "ND": 144.24, "PM": 145, "SM": 150.36, "EU": 151.964,
            "GD": 157.25, "TB": 158.9253, "DY": 162.5, "HO": 164.9303, "ER": 167.259,
             "TM": 168.9342, "YB": 173.04, "LU": 174.967, "HF": 178.49, "TA": 180.9479,
              "W": 183.84, "RE": 186.207, "OS": 190.23, "IR": 192.217, "PT": 195.078,
               "AU": 196.9665, "HG": 200.59, "TL": 204.3833, "PB": 207.2, "BI": 208.9804,
                "PO": 209, "AT": 210, "RN": 222, "FR": 223, "RA": 226, "AC": 227,
                 "PA": 231.0359, "TH": 232.0381, "NP": 237, "U": 238.0289, "AM": 243,
                  "PU": 244, "CM": 247, "BK": 247, "CF": 251, "ES": 252, "FM": 257,
                   "MD": 258, "NO": 259, "RF": 261, "LR": 262, "DB": 262, "BH": 264,
                    "SG": 266, "MT": 268, "RG": 272, "HS": 277}
