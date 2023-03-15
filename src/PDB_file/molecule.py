import re
import math
import atom

class Molecule:
    def __init__(self, atoms, amount=1) -> None:
        self.atoms = atoms
        self.count = amount
        name = atoms[0].resname
        same_name = False
        for atom in atoms:
            if atom.resname == name:
                same_name = True
            else:
                same_name = False
                break
        if same_name == False:
            print("Warning: Atoms in molecule object belongs to different residues.")
