import unittest
import sys
sys.path.append(".")
import pybiomol

class ChemTest(unittest.TestCase):

    def get_atom(self, element="C", atom_id=1, xyz=(10, 10, 10), name=None):
        atom = pybiomol.Atom(element, atom_id, *xyz, name=name)
        return atom



class AtomTest(ChemTest):

    def test_can_make_atom(self):
        atom = self.get_atom()
        self.assertIsInstance(atom, pybiomol.Atom)
        self.assertIsInstance(atom.element, str)
        self.assertIsInstance(atom.atom_id, int)
        self.assertIsInstance(atom.x, float)
        self.assertIsInstance(atom.y, float)
        self.assertIsInstance(atom.z, float)
        self.assertIsInstance(atom.name, str)
        self.assertEqual(atom.name, atom.element)
        str(atom)


    def test_can_make_atom_with_name(self):
        atom = self.get_atom(name="AT1")
        self.assertEqual(atom.name, "AT1")


    def test_can_get_distance_between_atoms(self):
        atom1 = self.get_atom(xyz=(-0.791, 64.789, 30.59)) # Atom 2621 in 1LOL
        atom2 = self.get_atom(xyz=(5.132, 63.307, 56.785)) # Atom 1011 in 1LOL
        pymol_calculated_distance = 26.9
        self.assertAlmostEqual(
         atom1.distance_to(atom2),
         pymol_calculated_distance,
         delta=0.01
        )


    def test_can_get_mass(self):
        atom = self.get_atom()
        self.assertAlmostEqual(atom.get_mass(), 12, delta=0.5)
        atom = self.get_atom(element="Ba")
        self.assertAlmostEqual(atom.get_mass(), 137, delta=0.5)
        atom = self.get_atom(element="XXX")
        self.assertEqual(atom.get_mass(), 0)



class AtomicStructureTest(ChemTest):

    def test_can_make_atomic_structure(self):
        atom1 = self.get_atom()
        atom2 = self.get_atom(element="N", xyz=(20, 20, 20))
        atomic_structure = pybiomol.AtomicStructure(atom1, atom2)
        self.assertIsInstance(atomic_structure, pybiomol.AtomicStructure)
        self.assertIsInstance(atomic_structure.atoms, list)
        for atom in atomic_structure.atoms:
            self.assertIsInstance(atom, pybiomol.Atom)
            self.assertIn(atom, (atom1, atom2))
        str(atomic_structure)


    def test_can_get_mass(self):
        atom1 = self.get_atom()
        atom2 = self.get_atom(element="N", xyz=(20, 20, 20))
        atomic_structure = pybiomol.AtomicStructure(atom1, atom2)
        self.assertEqual(
         atomic_structure.get_mass(),
         atom1.get_mass() + atom2.get_mass()
        )


    def test_atomic_structure_will_only_accept_atoms(self):
        self.assertRaises(
         AssertionError,
         lambda: pybiomol.AtomicStructure(self.get_atom(), "a string")
        )


    def test_can_make_molecule(self):
        atom1 = self.get_atom()
        atom2 = self.get_atom(element="N", xyz=(20, 20, 20))
        atom1.covalent_bond_to(atom2)
        molecule = pybiomol.Molecule(atom1, atom2)
        self.assertIsInstance(molecule, pybiomol.Molecule)


    def test_can_only_make_molecule_with_joined_atoms(self):
        atom1 = self.get_atom()
        atom2 = self.get_atom(element="N", xyz=(20, 20, 20))
        self.assertRaises(
         AssertionError,
         lambda: pybiomol.Molecule(atom1, atom2)
        )


    def test_can_get_atom_by_name(self):
        atom1 = self.get_atom(name="AAA")
        atom2 = self.get_atom(name="AAA")
        atom3 = self.get_atom(name="BBB")
        atomic_structure = pybiomol.AtomicStructure(atom1, atom2, atom3)
        self.assertEqual(atomic_structure.get_atom_by_name("AAA"), atom1)
        self.assertEqual(atomic_structure.get_atom_by_name("BBB"), atom3)



    def test_can_get_atom_by_number(self):
        atom1 = self.get_atom(atom_id=1)
        atom2 = self.get_atom(atom_id=2)
        atom3 = self.get_atom(atom_id=3)
        atomic_structure = pybiomol.AtomicStructure(atom1, atom3, atom2)
        self.assertEqual(atomic_structure.get_atom_by_id(1), atom1)
        self.assertEqual(atomic_structure.get_atom_by_id(2), atom2)
        self.assertEqual(atomic_structure.get_atom_by_id(3), atom3)



class BondTest(ChemTest):

    def test_can_make_bond(self):
        atom1 = self.get_atom()
        atom2 = self.get_atom(element="N", xyz=(20, 20, 20))
        bond = pybiomol.Bond(atom1, atom2)
        self.assertIsInstance(bond, pybiomol.Bond)
        self.assertIsInstance(bond.atoms, set)
        self.assertEqual(len(bond.atoms), 2)
        for atom in bond.atoms:
            self.assertIsInstance(atom, pybiomol.Atom)
            self.assertIn(atom, (atom1, atom2))
        str(bond)


    def test_can_get_bond_distance(self):
        atom1 = self.get_atom()
        atom2 = self.get_atom(element="N", xyz=(20, 20, 20))
        bond = pybiomol.Bond(atom1, atom2)
        self.assertEqual(
         bond.get_length(),
         atom1.distance_to(atom2)
        )


    def test_can_create_covalent_bond(self):
        atom1 = self.get_atom()
        atom2 = self.get_atom(element="N", xyz=(20, 20, 20))
        covalent_bond = pybiomol.CovalentBond(atom1, atom2)
        self.assertIsInstance(covalent_bond, pybiomol.CovalentBond)
        self.assertIsInstance(covalent_bond, pybiomol.Bond)


    def test_can_bond_atoms_together(self):
        atom1 = self.get_atom()
        atom2 = self.get_atom(element="N", xyz=(20, 20, 20))
        atom1.covalent_bond_to(atom2)
        self.assertEqual(len(atom1.covalent_bonds), 1)
        self.assertEqual(len(atom2.covalent_bonds), 1)
        self.assertIs(atom1.covalent_bonds[0], atom2.covalent_bonds[0])
        self.assertEqual(len(atom1.get_covalently_bonded_atoms()), 1)
        self.assertEqual(len(atom2.get_covalently_bonded_atoms()), 1)
        self.assertIs(atom1.get_covalently_bonded_atoms()[0], atom2)
        self.assertIs(atom2.get_covalently_bonded_atoms()[0], atom1)
        atom3 = self.get_atom(element="C", xyz=(30, 30, 30))
        atom2.covalent_bond_to(atom3)
        self.assertEqual(len(atom2.covalent_bonds), 2)
        self.assertEqual(len(atom3.covalent_bonds), 1)
        self.assertEqual(len(atom2.get_covalently_bonded_atoms()), 2)
        self.assertEqual(len(atom3.get_covalently_bonded_atoms()), 1)


    def test_can_only_covalently_bond_atoms_to_other_atoms(self):
        atom = self.get_atom()
        self.assertRaises(
         AssertionError,
         lambda: atom.covalent_bond_to("a string")
        )


    def test_can_get_all_covalently_accessible_atoms(self):
        atom1 = self.get_atom(name="atom1")
        atom2 = self.get_atom(name="atom2")
        atom3 = self.get_atom(name="atom3")
        atom4 = self.get_atom(name="atom4")
        atom5 = self.get_atom(name="atom5")
        atom6 = self.get_atom(name="atom6")
        atom7 = self.get_atom(name="atom7")
        atom8 = self.get_atom(name="atom8")
        atom9 = self.get_atom(name="atom9")
        atom10 = self.get_atom(name="atom10")
        atom11 = self.get_atom(name="atom11")
        atom1.covalent_bond_to(atom2)
        atom1.covalent_bond_to(atom3)
        atom4.covalent_bond_to(atom2)
        atom4.covalent_bond_to(atom3)
        atom1.covalent_bond_to(atom5)
        atom5.covalent_bond_to(atom6)
        atom5.covalent_bond_to(atom8)
        atom6.covalent_bond_to(atom7)
        atom8.covalent_bond_to(atom9)
        atom4.covalent_bond_to(atom10)
        atom4.covalent_bond_to(atom11)
        self.assertEqual(
         len(atom1.get_covalently_accessible_atoms()),
         10
        )
        self.assertEqual(
         set(atom1.get_covalently_accessible_atoms()),
         set((atom2, atom3, atom4, atom5, atom6, atom7, atom8, atom9, atom10, atom11))
        )



if __name__ == "__main__":
    unittest.main()
