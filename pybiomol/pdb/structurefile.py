import types
from ..structure import chemstructure
from ..structure import macrostructure
from .residues import connection_data as _conn_data

class Pdb:

    def __init__(self, data_file):
        self.data_file = data_file

        transfer_attrs = [
         "classification",
         "deposition_date",
         "pdb_code",
         "is_obsolete",
         "obsolete_date",
         "replacement_code",
         "title",
         "split_codes",
         "caveat",
         "keywords",
         "experimental_techniques",
         "model_num",
         "model_annotations",
         "authors",
         "revisions",
         "supercedes",
         "supercede_date",
         "journal"
        ]
        for attr in transfer_attrs:
            self.__dict__[attr] = self.data_file.__dict__[attr]

        self.small_molecule_types = []
        for het in set(list(self.data_file.het_names.keys())
         + list(self.data_file.het_formulae.keys())):
            het_class = types.new_class(het, bases=(PdbSmallMolecule,))
            het_class.het_code = het
            het_class.het_name = self.data_file.het_names.get(het)
            het_class.het_formula = self.data_file.het_formulae.get(het)["formula"]
            het_class.is_water = self.data_file.het_formulae.get(het)["is_water"]
            het_class.synonyms = self.data_file.het_synonyms.get(het)
            het_class.__repr__ = lambda h: "<%s molecule>" % h.het_code
            self.small_molecule_types.append(het_class)

        model_numbers = [
         model["model_num"] for model in self.data_file.models
        ] if self.data_file.models else [1]
        self.models = [PdbModel(self.data_file, num, self) for num in model_numbers]
        self.model = self.models[0]


    def __repr__(self):
        return "<Pdb (%s)>" % (self.pdb_code if self.pdb_code else "????")


    def get_small_molecule_type_by_code(self, code):
        for small_molecule_type in self.small_molecule_types:
            if small_molecule_type.het_code == code:
                return small_molecule_type
        return PdbSmallMolecule



class PdbModel(chemstructure.AtomicStructure):

    def __init__(self, data_file, model_num, pdb):
        self.pdb = pdb
        self._create_atoms(data_file, model_num)
        self._create_explicit_bonds(data_file)
        self._create_implicit_bonds(data_file, model_num)
        self._create_small_molecules(data_file, model_num)
        self._create_residues(data_file, model_num)


    def _create_atoms(self, data_file, model_num):
        atom_dicts = [
         a_dict for a_dict in data_file.atoms if a_dict["model"] == model_num
        ]
        hetatom_dicts = [
         h_dict for h_dict in data_file.heteroatoms if h_dict["model"] == model_num
        ]
        anisou_dicts = [
         a_dict for a_dict in data_file.anisou if a_dict["model"] == model_num
        ]
        atom_ids = sorted(list(set([a["number"] for a in atom_dicts])))
        hetatom_ids = sorted(list(set([h["number"] for h in hetatom_dicts])))
        self.macro_atoms = []
        for atom_id in atom_ids:
            anisou = [a_dict for a_dict in anisou_dicts if a_dict["number"] == atom_id]
            self.macro_atoms.append(PdbAtom(
             [a_dict for a_dict in atom_dicts if a_dict["number"] == atom_id][0],
             self,
             anisou[0] if anisou else None
            ))
        self.hetero_atoms = []
        for hetatom_id in hetatom_ids:
            anisou = [a_dict for a_dict in anisou_dicts if a_dict["number"] == hetatom_id]
            self.hetero_atoms.append(PdbHetAtom(
             [h_dict for h_dict in hetatom_dicts if h_dict["number"] == hetatom_id][0],
             self,
             anisou[0] if anisou else None
            ))
        all_atoms = self.macro_atoms + self.hetero_atoms
        chemstructure.AtomicStructure.__init__(self, *all_atoms)


    def _create_explicit_bonds(self, data_file):
        for connection in data_file.connections:
            for bonded_atom in connection["bonded_atoms"]:
                self.get_atom_by_id(connection["atom_number"]
                 ).covalent_bond_to(self.get_atom_by_id(bonded_atom))


    def _create_implicit_bonds(self, data_file, model_num):
        for atom in data_file.atoms:
            residue_mates = [a for a in data_file.atoms
             if a["chain"] == atom["chain"]
              and a["residue_number"] == atom["residue_number"]
               and a["model"] == model_num]
            bond_atom_names = _conn_data.get(atom["residue_name"], {}
             ).get(atom["name"], [])
            for name in bond_atom_names:
                bonded_atom = [a for a in residue_mates if a["name"] == name]
                bonded_atom = bonded_atom[0] if bonded_atom else None
                if bonded_atom:
                    self.get_atom_by_id(atom["number"]).covalent_bond_to(
                     self.get_atom_by_id(bonded_atom["number"]))

        for chain in sorted(list(set([a["chain"] for a in data_file.atoms]))):
            residue_numbers = sorted(list(set([a["residue_number"]
             for a in data_file.atoms if a["chain"] == chain and a["model"] == model_num])))
            for index, residue_number in enumerate(residue_numbers[:-1]):
                carboxyl_atom_number = [a["number"] for a in data_file.atoms
                 if a["residue_number"] == residue_number and a["name"] == "C"]
                carboxyl_atom_number = carboxyl_atom_number[0]\
                 if carboxyl_atom_number else None
                next_amino_nitrogen_number = [a["number"] for a in data_file.atoms
                 if a["residue_number"] == residue_numbers[index+1]
                  and a["name"] == "N"]
                next_amino_nitrogen_number = next_amino_nitrogen_number[0]\
                 if next_amino_nitrogen_number else None
                if carboxyl_atom_number != None and next_amino_nitrogen_number != None:
                    self.get_atom_by_id(carboxyl_atom_number).covalent_bond_to(
                     self.get_atom_by_id(next_amino_nitrogen_number))


    def _create_small_molecules(self, data_file, model_num):
        self.small_molecules = []
        residue_numbers = sorted(list(set([a["residue_number"]
         for a in data_file.heteroatoms])))
        for residue_number in residue_numbers:
            het_code = [a["residue_name"] for a in data_file.heteroatoms
             if a["residue_number"] == residue_number][0]
            atom_numbers = [a["number"] for a in data_file.heteroatoms
             if a["residue_number"] == residue_number and a["model"] == model_num]
            molecule_type = self.pdb.get_small_molecule_type_by_code(het_code)
            self.small_molecules.append(
             molecule_type(*[self.get_atom_by_id(number) for number in atom_numbers])
            )


    def _create_residues(self, data_file, model_num):
        self.residues = []
        residue_numbers = sorted(list(set([a["residue_number"]
         for a in data_file.atoms])))
        for residue_number in residue_numbers:
            residue_name = [a["residue_name"] for a in data_file.atoms
             if a["residue_number"] == residue_number][0]
            atom_numbers = [a["number"] for a in data_file.atoms
             if a["residue_number"] == residue_number and a["model"] == model_num]
            self.residues.append(PdbResidue(
             residue_number,
             residue_name,
             *[self.get_atom_by_id(number) for number in atom_numbers])
            )


    def __repr__(self):
        return "<PdbModel (%i atoms, %.2f Da)>" % (len(self.atoms), self.get_mass())




class PdbAtom(chemstructure.Atom):

    def __init__(self, atom_dict, model, anisous_dict=None):
        chemstructure.Atom.__init__(
         self,
         atom_dict["element"],
         atom_dict["number"],
         atom_dict["x"],
         atom_dict["y"],
         atom_dict["z"],
         atom_dict["name"]
        )
        self.charge = atom_dict["charge"]
        self.u11 = anisous_dict["u11"] if anisous_dict else None
        self.u22 = anisous_dict["u22"] if anisous_dict else None
        self.u33 = anisous_dict["u33"] if anisous_dict else None
        self.u12 = anisous_dict["u12"] if anisous_dict else None
        self.u13 = anisous_dict["u13"] if anisous_dict else None
        self.u23 = anisous_dict["u23"] if anisous_dict else None
        self.residue = None
        self.chain = None
        self.model = model



class PdbHetAtom(PdbAtom):

    def __init__(self, *args, **kwargs):
        PdbAtom.__init__(self, *args, **kwargs)
        self.molecule = None
        del self.__dict__["residue"]
        del self.__dict__["chain"]



class PdbSmallMolecule(chemstructure.Molecule):

    def __init__(self, *atoms):
        chemstructure.Molecule.__init__(self, *atoms)
        for atom in self.atoms:
            atom.molecule = self



class PdbResidue(macrostructure.Residue):

    def __init__(self, residue_id, *args, **kwargs):
        self.residue_id = residue_id
        macrostructure.Residue.__init__(self, *args, **kwargs)
        for atom in self.atoms:
            atom.residue = self
