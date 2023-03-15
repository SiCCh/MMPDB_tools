import math
import re
import copy
import atom
import bond


class PDB_file:
    def __init__(self, file_path='', read_parameters=True) -> None:
        self.atoms = []
        self.bonds = []
        self.parameters = {'masses': [],
                            'bonds': [],
                            'angles': [],
                            'dihedrals': [],
                            'nonbonded': []}
        self.box = {'a': 0.0,
                     'b': 0.0,
                     'c': 0.0,
                     'alpha': 0.0,
                     'beta': 0.0,
                     'gamma': 0.0}
        self.datfile = ''
        if file_path != '':
            with open(file_path, 'r') as pdb:
                probable_parameters = []
                for line in pdb.readlines():
                    if line.startswith('#'):
                        pass
                    elif line.startswith('ATOM') or line.startswith('HETATM'):
                        new_atom = atom.Atom(line=line, fromline=True)
                        self.atoms.append(new_atom)
                    elif line.startswith('CONN') or line.startswith('CONECT'):
                        new_bond = bond.Bond(line=line, fromline=True)
                        self.bonds.append(new_bond)
                    elif line.startswith('BOX'):
                        self.box = self.read_box(line)
                    elif line.startswith('DAT'):
                        self.datfile = line
                    elif read_parameters == True:
                        probable_parameters += [line]
                if read_parameters == True:
                    self.parameters = self.classify_parameters(lines=probable_parameters)
            self.share_atom_type()
    
    def classify_parameters(self, lines):
        atom_type_dihedrals_regex = re.compile(r'([a-zA-Z0-9\s]{2})-([a-zA-Z0-9\s]{2})-([a-zA-Z0-9\s]{2})-([a-zA-Z0-9\s]{2})')
        mass_list = []
        bond_list = []
        angle_list = []
        dihedral_list = []
        dihedral_preformat = []
        nonbonded_list = []
        parameter_type = ''
        for line in lines:
            if line.startswith('MASS'):
                parameter_type = 'mass'
                pass
            elif line.startswith('BOND'):
                parameter_type = 'bond'
                pass
            elif line.startswith('ANGL'):
                parameter_type = 'angle'
                pass
            elif line.startswith('DIHE'):
                parameter_type = 'dihedral'
                pass
            elif line.startswith('NONB'):
                parameter_type = 'nonbonded'
                pass
            elif line.startswith('END'):
                parameter_type='end'
                pass
            if parameter_type == 'mass' and not line.startswith('MASS'):
                mass_list += [self.format_mass_parameter(line)]
            elif parameter_type == 'bond' and not line.startswith('BOND'):
                bond_list += [self.format_bond_parameter(line)]
            elif parameter_type == 'angle' and not line.startswith('ANGL'):
                angle_list += [self.format_angle_parameter(line)]
            elif parameter_type == 'dihedral' and not line.startswith('DIHE'):
                if re.findall(atom_type_dihedrals_regex, line) and len(dihedral_preformat) == 0:
                    dihedral_preformat += [line]
                elif not re.findall(atom_type_dihedrals_regex, line) and len(dihedral_preformat) != 0:
                    dihedral_preformat += [line]
                elif re.findall(atom_type_dihedrals_regex, line) and len(dihedral_preformat) != 0:
                    dihedral_list += [self.format_dihedral_parameter(dihedral_preformat)]
                    dihedral_preformat.clear()
                    dihedral_preformat += [line]
                else:
                    dihedral_preformat += [line]
                    dihedral_list += [self.format_dihedral_parameter(dihedral_preformat)]
                    dihedral_preformat.clear()                
            elif parameter_type == 'nonbonded' and not line.startswith('NONB'):
                nonbonded_list += [self.format_nonbonded_parameter(line)]
            if len(dihedral_preformat) != 0 and (parameter_type == 'end' or parameter_type == 'nonbonded'):
                    dihedral_list += [self.format_dihedral_parameter(dihedral_preformat)]
                    dihedral_preformat.clear()
        return {'mass_parameters': mass_list,
                'bond_parameters': bond_list,
                'angle_parameters': angle_list,
                'dihedral_parameters': dihedral_list,
                'nonbonded_parameters': nonbonded_list}
    
                
    def format_mass_parameter(self, line):
        fields = line.split()
        return  {'atom_type': fields[0],
                 'mass': fields[1],
                 'polarisability': fields[2]}
        
    def format_bond_parameter(self, line):
        atom_types = re.findall(r'([a-zA-Z0-9\s]{2})-([a-zA-Z0-9\s]{2})', line)[0]
        if not atom_types:
            raise ValueError("Could not find atom types in line: " + line)
        values = line[5:].split()
        return {'atom_1': atom_types[0],
                'atom_2': atom_types[1],
                'eq_dist': values[0],
                'force': values[1]}
        
    def format_angle_parameter(self, line):
        atom_types = re.findall(r'([a-zA-Z0-9\s]{2})-([a-zA-Z0-9\s]{2})-([a-zA-Z0-9\s]{2})', line)[0]
        if not atom_types:
            raise ValueError("Could not find atom types in line: " + line)
        values = line[9:].split()
        return {'atom_1': atom_types[0],
                'atom_2': atom_types[1],
                'atom_3': atom_types[2],
                'eq_angle': values[0],
                'force': values[1]}

    def format_dihedral_parameter(self, lines):
        list_of_dihedral_parameters = []
        dihedral_parameter = {'atom1': '',
                              'atom2': '',
                              'atom3': '',
                              'atom4': '',
                              '1-4_vdw': 0,
                              '1-4_coul': 0,
                              'values': []}
        for line in lines:
            atom_types = re.findall(r'([a-zA-Z0-9\s]{2})-([a-zA-Z0-9\s]{2})-([a-zA-Z0-9\s]{2})-([a-zA-Z0-9\s]{2})', line)
            values = line[12:].split()
            param_values = {'div_factor': int(values[0]),
                            'eq_angle': float(values[1]),
                            'phase': float(values[2]),
                            'periodicity': int(values[3])}
            if len(atom_types) > 0:
                atom_types=atom_types[0]
                dihedral_parameter['atom1'] = atom_types[0]
                dihedral_parameter['atom2'] = atom_types[1]
                dihedral_parameter['atom3'] = atom_types[2]
                dihedral_parameter['atom4'] = atom_types[3]
                dihedral_parameter['1-4_vdw'] = float(values[4])
                dihedral_parameter['1-4_coul'] = float(values[5])
            if param_values['periodicity'] < 0:
                dihedral_parameter['values'].append(param_values)
            else:
                dihedral_parameter['values'].append(param_values)
                list_of_dihedral_parameters.append(dihedral_parameter)  
        return list_of_dihedral_parameters
        
    def format_nonbonded_parameter(self, line):
        fields = line.split()
        format = ''
        if len(fields) == 3:
            format = 'type, r, epsilon'
        elif len(fields) == 4:
            format = 'type1, type2, Acoeff, Bcoeff'
        if format == 'type, r, epsilon':
            return {'format': format,
                    'atom_type': fields[0],
                    'r': fields[1],
                    'epsilon': fields[2]
                    }
        elif format == 'type1, type2, Acoeff, Bcoeff':
            return {'format': format,
                    'atom_type_1': fields[0],
                    'atom_type_2': fields[1],
                    'Acoeff': fields[2],
                    'Bcoeff': fields[3]
                    }
    
    def share_atom_type(self, verbose=False):
        for atom in self.atoms:
            for bond in self.bonds:
                if atom.number == bond.center:
                    if atom.type == None and bond.atom_type != None:
                        atom.type = bond.atom_type
                        if verbose==True:
                            print(f"New atom type found for atom {atom.number} - {atom.name} : {atom.type}")
                    elif bond.atom_type == None and atom.type != None:
                        bond.atom_type = atom.type
                        if verbose==True:
                            print(f"New atom type found for atom {atom.number} - {atom.name} : {atom.type}")
                    elif atom.type == None and bond.atom_type == None:
                        if verbose==True:
                            print(f"No atom type found for atom {atom.number} - {atom.name}")
                    elif (atom.type != None and bond.atom_type != None) and atom.type != bond.atom_type:
                        if verbose==True:
                            print(f"Atom type mismatch between bond and atom information for atom {atom.number} - {atom.name}\nAtom type from atom: {atom.type}\nAtom type from bond: {bond.atom_type}")
                    
    def read_box(self, line):
        box_field = line.split()
        box_x = float(box_field[1])
        box_y = float(box_field[2])
        box_z = float(box_field[3])
        if len(line.split()) > 5:
            alpha = float(box_field[4])
            beta = float(box_field[5])
            gamma = float(box_field[6])
        else:
            alpha = float(box_field[4])
            beta = alpha
            gamma = alpha
        return {'a': box_x, 'b': box_y, 'c': box_z, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
    
    def box_volume(self, box):
        a = box['a']
        b = box['b']
        c = box['c']
        alpha = box['alpha']
        beta = box['beta']
        gamma = box['gamma']
        return (a*b*c*(1 - math.cos(alpha)**2 - math.cos(beta)**2 - math.cos(gamma)**2 + 2*math.cos(alpha)*math.cos(beta)*math.cos(gamma))**0.5)
    
    def total_charge(self):
        total_charge = 0
        for atom in self.atoms:
            total_charge += atom.charge
        total_charge = round(total_charge, 8)
        return total_charge
    
    def dipole_moment(self):
        for atom in self.atoms:
            if atom.name == 'O':
                print(atom.name, atom.charge)
                
    def format_nicely(self):
        ## Format the PDB (xdraw style) and return a list of lines (printable, exportable...)
        lines = []
        for atom in self.atoms:
            lines += [f"ATOM    {format(atom.number, '>3')} {format(atom.name, '<5')} {format(atom.resname, '<3')}     {format(atom.resnumber, '<3')}     "]
            if atom.x >= 0:
                lines[-1] += f" {atom.x:6.6f}  "
            else:
                lines[-1] += f"{atom.x:6.6f}  "
            if atom.y >= 0:
                lines[-1] += f" {atom.y:6.6f}  "
            else:
                lines[-1] += f"{atom.y:6.6f}  "
            if atom.z >= 0:
                lines[-1] += f" {atom.z:6.6f}  "
            else:
                lines[-1] += f"{atom.z:6.6f}  "
            if atom.charge >= 0:
                lines[-1] += f" {atom.charge:6.6f}"
            else:
                lines[-1] += f"{atom.charge:6.6f}"
        lines += ["END"]
        for bond in self.bonds:
            lines += [f"CONN    {format(bond.center, '>3')} {format(bond.atom_type, '<2')}   "]
            for bonded_atom in bond.bonded_atoms:
                lines[-1] += f"{bonded_atom} "
        lines += ["END"]
        lines += ["# MM parameters"]
        for key in self.parameters.keys():
            if key == "mass_parameters" and len(self.parameters[key]) > 0:
                lines += ["MASS"]
                for item in self.parameters[key]:
                    lines += [f"{format(item['atom_type'], '<2')}     {float(item['mass']):6.3f} {float(item['polarisability']):6.3f}"]
            if key == 'bond_parameters' and len(self.parameters[key]) > 0:
                lines += ["BOND"]
                for item in self.parameters[key]:
                    lines += [f"{format(item['atom_1'], '<2')}-{format(item['atom_2'], '<2')}  {float(item['eq_dist']):6.3f} {float(item['force']):5.4f}"]
            if key == 'angle_parameters' and len(self.parameters[key]) > 0:
                lines += ["ANGL"]
                for item in self.parameters[key]:
                    lines += [f"{format(item['atom_1'], '<2')}-{format(item['atom_2'], '<2')}-{format(item['atom_3'], '<2')}   {float(item['eq_angle']):6.3f}  {float(item['force']):6.3f}"]
            if key == 'dihedral_parameters' and len(self.parameters[key]) > 0:
                lines += ["DIHE"]
                for item in self.parameters[key]:
                    for dihedral in item:
                        lines += [f"{format(dihedral['atom1'], '<2')}-{format(dihedral['atom2'], '<2')}-{format(dihedral['atom3'], '<2')}-{format(dihedral['atom4'], '<2')} {int(dihedral['values'][0]['div_factor']):>2d} {float(dihedral['values'][0]['eq_angle']):>6.3f} {float(dihedral['values'][0]['phase']):>6.2f} {int(dihedral['values'][0]['periodicity']):>2d} {float(dihedral['1-4_vdw']):6.3f} {float(dihedral['1-4_coul']):6.3f}"]
                        if len(dihedral['values']) > 1:
                            for i in range(1, len(dihedral['values'])):
                                lines += [f"            {int(dihedral['values'][i]['div_factor']):>2d} {float(dihedral['values'][i]['eq_angle']):>6.3f} {float(dihedral['values'][i]['phase']):>6.2f} {int(dihedral['values'][i]['periodicity']):>2d}"]
            if key == 'nonbonded_parameters' and len(self.parameters[key]) > 0:
                lines += ["NONB"]
                for item in self.parameters[key]:
                    if item['format'] == 'type, r, epsilon':
                        lines += [f"{format(item['atom_type'], '<2')}  {float(item['r']):6.4f}  {float(item['epsilon']):6.4f}"]
                    elif item['format'] == 'type_1, type_2, Acoeff, Bcoeff':
                        lines += [f"{format(item['atom_type_1'], '<2')} {format(item['atom_type_2'], '<2')} {float(item['Acoeff']):6.4f}  {float(item['Bcoeff']):6.4f}"]
        lines += ["END"]
        if self.box != []:
            lines += [(f"BOX {self.box['a']} {self.box['b']} {self.box['c']} {self.box['alpha']} {self.box['beta']} {self.box['gamma']}")]
        lines += ["END"]
        if self.datfile != []:
            lines += [self.datfile]
        return lines
    
    def export_to_pdb(self, pdb_file='output.pdb'):
        ### Export the PDB object to a PDB file
        lines = self.format_nicely()
        with open(pdb_file, 'w') as f:
            for line in lines:
                f.writelines(line+'\n')
        print("PDB exported to file: "+pdb_file)
    
    def print(self):
        lines = self.format_nicely()
        for line in lines:
            print(line)

def scale_charges(pdb, scale_factor):
    ### Scale the charges of a clone of the PDB object by a scaling factor
    ## Return the new PDB object
    modified_pdb = copy.deepcopy(pdb)
    for atom in modified_pdb.atoms:
        atom.charge = atom.charge*scale_factor
    return modified_pdb

def mix_charges(pdb1, pdb2, ratio=0.5):
    ### Clone a PDB object and replace the charges of the clone by a weighted combination of its original charges and the charges of another PDB object
    ##  (ex: ratio=0.1 means that the new charge will be 10% of the original charge and 90% of the source charge)
    ## Return the new PDB object
    modified_pdb = copy.deepcopy(pdb1)
    for atom1 in modified_pdb.atoms:
        for atom2 in pdb2.atoms:
            if atom1.name == atom2.name:
                new_charge = atom1.charge*(ratio) + atom2.charge*(1-ratio)
                new_charge = round(new_charge, 6)
                atom1.charge = new_charge
    return modified_pdb

def swap_charges(original, source):
    return mix_charges(original, source, 1.0)
                

## Implement a converter for LJ/WH rules
