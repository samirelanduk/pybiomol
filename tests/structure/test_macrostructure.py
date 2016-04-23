import unittest
import sys
sys.path.append(".")
import pybiomol
from test_chemstructure import ChemTest

class MacroTest(ChemTest):

    def get_residue(self):
        atoms = [self.get_atom() for _ in range(10)]
        for index, atom in enumerate(atoms[:-1]):
            atom.covalent_bond_to(atoms[index+1])
        residue = pybiomol.Residue("VAL", atoms)
        return residue


class ResidueTest(MacroTest):

    def test_can_make_resiude(self):
        residue = self.get_residue()
        str(residue)



class ResiduicStructureTest(MacroTest):

    def test_can_make_residuic_structure(self):
        residues = [self.get_residue() for _ in range(10)]
        residuic_structure = pybiomol.ResiduicStructure(residues)
        str(residuic_structure)



class ResidueSequenceTest(MacroTest):

    def test_can_make_residuic_sequence(self):
        residues = [self.get_residue() for _ in range(10)]
        for index, residue in enumerate(residues[:-1]):
            residue.atoms[-1].covalent_bond_to(residues[index + 1].atoms[0])
        residue_sequence = pybiomol.ResidueSequence(residues)
        str(residue_sequence)



class ProteinChainTest(MacroTest):

    def test_can_make_protein_chain(self):
        residues = [self.get_residue() for _ in range(10)]
        for index, residue in enumerate(residues[:-1]):
            residue.atoms[-1].covalent_bond_to(residues[index + 1].atoms[0])
        chain = pybiomol.ProteinChain("A", residues)
        str(chain)



class BindingSiteTest(MacroTest):

    def test_can_make_binding_site_without_ligand(self):
        residues = [self.get_residue() for _ in range(10)]
        site = pybiomol.BindingSite(residues)
        self.assertTrue(site.ligand is None)
        str(site)


    def test_can_make_binding_site_with_ligand(self):
        residues = [self.get_residue() for _ in range(10)]
        ligand = self.get_atom()
        site = pybiomol.BindingSite(residues, ligand)
        self.assertTrue(site.ligand is ligand)
        str(site)



class AlphaHelixTest(MacroTest):

    def test_can_make_alpha_helix(self):
        residues = [self.get_residue() for _ in range(10)]
        for index, residue in enumerate(residues[:-1]):
            residue.atoms[-1].covalent_bond_to(residues[index + 1].atoms[0])
        chain = pybiomol.ProteinChain("A", residues)
        helix_residues = chain.residues[1:6]
        helix = pybiomol.AlphaHelix(helix_residues, chain)
        self.assertTrue(helix.chain is chain)
        self.assertTrue(chain.alpha_helices[0] is helix)
        str(helix)


    def test_cannot_make_helix_with_wrong_chain(self):
        residues = [self.get_residue() for _ in range(10)]
        for index, residue in enumerate(residues[:-1]):
            residue.atoms[-1].covalent_bond_to(residues[index + 1].atoms[0])
        chain = pybiomol.ProteinChain("A", residues)
        helix_residues = [self.get_residue() for _ in range(5)]
        self.assertRaises(
         AssertionError,
         lambda: pybiomol.AlphaHelix(helix_residues, chain)
        )

if __name__ == "__main__":
    unittest.main()
