from ..structure import chemstructure
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

        model_numbers = [
         model["model_num"] for model in self.data_file.models
        ] if self.data_file.models else [1]
        self.models = [PdbModel(self.data_file, num) for num in model_numbers]
        self.model = self.models[0]


    def __repr__(self):
        return "<Pdb (%s)>" % (self.pdb_code if self.pdb_code else "????")



class PdbModel(chemstructure.AtomicStructure):

    def __init__(self, data_file, model_num):
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

        for connection in data_file.connections:
            for bonded_atom in connection["bonded_atoms"]:
                self.get_atom_by_id(connection["atom_number"]
                 ).covalent_bond_to(self.get_atom_by_id(bonded_atom))

        for atom in data_file.atoms:
            residue_mates = [a for a in data_file.atoms if a["chain"] == atom["chain"] and a["residue_number"] == atom["residue_number"]]
            bond_atom_names = _conn_data.get(atom["residue_name"], {}).get(atom["name"], [])
            for name in bond_atom_names:
                bonded_atom = [a for a in residue_mates if a["name"] == name]
                bonded_atom = bonded_atom[0] if bonded_atom else None
                if bonded_atom:
                    self.get_atom_by_id(atom["number"]).covalent_bond_to(self.get_atom_by_id(bonded_atom["number"]))



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
        self.ligand = None
        del self.__dict__["residue"]
        del self.__dict__["chain"]
