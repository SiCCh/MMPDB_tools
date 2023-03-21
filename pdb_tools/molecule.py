import math

class Molecule:
    def __init__(self, atoms, amount=1) -> None:
        self.amount = amount
        self.atoms = []
        name = atoms[0].resname
        same_name = False
        self.total_charge = None
        total_charge = 0.0
        if atoms[0].charge != None:
            for atom in atoms:
                total_charge += atom.charge
            self.total_charge = round(total_charge, 6)
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
    
    def dipole_moment(self):
        ### Compute dipole moment from the atomic charges and coordinates in the molecule object.
        ## Return (dipole moment in Debye, dipole vector in e-.Angstrom)
        total_charge=0
        dipole_vector=[0.0,0.0,0.0]
        for atom in self.atoms:
            total_charge+=float(atom.charge)
            dipole_vector[0] += atom.charge*float(atom.x)
            dipole_vector[1] += atom.charge*float(atom.y)
            dipole_vector[2] += atom.charge*float(atom.z)
        dipole_moment=math.sqrt(dipole_vector[0]**2 + dipole_vector[1]**2 + dipole_vector[2]**2)
        dipole_moment=dipole_moment*(1/0.2081943) ## e-.Angstrom to Debye
        return (dipole_moment, dipole_vector)
