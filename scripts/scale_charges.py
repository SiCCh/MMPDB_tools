import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from PDB_file import pdb_file
import argparse

parser = argparse.ArgumentParser(
                    prog = 'PDB charges scaler',
                    description = 'Scale atom charges',
                    epilog = 'No more copypasting')

parser.add_argument('-p', '--pdb',
                    action='store',
                    default=None)
parser.add_argument('-s', '--scale',
                    action='store',
                    default=None)
parser.add_argument('-o', '--output',
                    action='store',
                    default="scaled_charges.pdb")
args=parser.parse_args()

pdb=args.inputA
scaling_factor=float(args.scale)

pdb = pdb_file.PDB_file(pdb1)
out = pdb_file.scale_charges(pdb, scaling_factor)
out.export_to_pdb(args.output)


