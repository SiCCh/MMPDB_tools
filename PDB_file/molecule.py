import re
import math
from .atom import Atom
class Molecule:
    def __init__(self, atoms, amount=1) -> None:
        self.amount = amount
        self.atoms = []
        name = atoms[0].resname
        same_name = False
        for atom in atoms:
            self.atoms += [atom]
            if atom.resname == name:
                same_name = True
            else:
                same_name = False
                break
        if same_name == False:
            print("Warning: Atoms in molecule object belongs to different residues.")
        self.name = name
