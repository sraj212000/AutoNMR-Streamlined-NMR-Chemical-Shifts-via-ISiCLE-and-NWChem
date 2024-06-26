from rdkit import Chem
from rdkit.Chem import AllChem
import subprocess
import time
import sys
import pandas as pd
import re
import os



def generate_3d_coordinates(smiles, output_file):
    molecule = Chem.MolFromSmiles(smiles)
    molecule = Chem.AddHs(molecule)
    AllChem.EmbedMolecule(molecule)
    AllChem.UFFOptimizeMolecule(molecule)

 
    with open(output_file, 'w') as f:
        # Print the initial lines
        f.write(f"start\n\ntitle \"{smiles}\"\n\necho\ngeometry {smiles}\n")
    
        # Retrieve the conformer once outside the loop
        conformer = molecule.GetConformer()
    
        # Loop over each atom in the molecule to print their positions
        for atom in molecule.GetAtoms():
            position = conformer.GetAtomPosition(atom.GetIdx())
            x, y, z = position.x, position.y, position.z
            f.write(f"   {atom.GetSymbol():<2s} {x:>10.8f} {y:>10.8f} {z:>10.8f}\n")
    
         # Print the end of the geometry section and other parts
        f.write(
        "end\n\n\nbasis spherical\n* library 6-311G\nend\n\n"
        "driver\n"
        "  tight\n  maxiter 200\n  xyz final\n"
        "end\n\n"
        "relativistic\n"
        "  zora on\n"
        "  zora:cutoff_NMR 1d-8\n"
        "  zora:cutoff 1d-30\n"
        "end\n\n"
        "dft\n"
        "  direct\n"
        "  grid fine\n"
        f" xc {xc_functional}\n"
        "  mult 1\n"
        '  noprint "final vectors analysis" multipole\n'
        "end\n\n"
        f"set geometry {smiles}\n"
        "task dft optimize\n\n"
        "property\n"
        "   shielding\n"
        "end\n\n"
        
        "cosmo\n"
        "   solvent cdcl3\n"
        "end\n\n"
        "task dft property\n"
        )

    
def run_nwchem(commands):
    print("Running NWChem...")
    start_time = time.time()
    subprocess.run(commands, shell=True)
    end_time = time.time()
    execution_time = end_time - start_time
    print("NWChem execution time: {:.2f} seconds".format(execution_time), file=sys.stderr)

def run(smile):
    # Make own character set and pass this as argument in compile method
    global output_file
    global output_file_name
    regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
    # Check for special characters in the string
    if regex.search(smile) is not None:
        smile = f'"{smile}"'   
    output_file = f"{smile}.nw"
    output_file_name = f"{smile}.out"    
    return output_file, output_file_name

print(" While Running the command Enter 1st argument as .xlsx file containing smiles code in single row ")

if len(sys.argv) > 3:
    print("Error in Argument Declaration")
elif len(sys.argv) == 1:
    print("Please enter the argument as .xlsx as asked above")
else:
    # Set default xc_functional to "pbe0"
    xc_functional = "pbe0"
    
    # Check if the second argument is provided
    if len(sys.argv) > 2:
        xc_functional = sys.argv[2]

# Assume xc_functional is a user input variable
# Example value, this should be set by the user


df = pd.read_excel(sys.argv[1], usecols='A')
l1 = []
for index, row in df.iterrows():
    l1.append(row.to_list())
length = len(l1)
for i in range(length):
	# Generate NWChem input and output file names
	smile=l1[i][0]
	output_file = "{}.nw".format(smile+" "+xc_functional)
	output_file_name = "{}.out".format(smile+" "+xc_functional)	
	generate_3d_coordinates(smile, output_file)
	run(smile+" "+xc_functional)
	# Build NWChem command
	nwchem_command = "nwchem {} > {}".format(output_file, output_file_name)
	# Build final command with additional options
	final_command = "mpiexec --use-hwthread-cpus -np 1 {}".format(nwchem_command)
	# Run NWChem with the provided command
	run_nwchem(final_command )

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Find all .out files in the script's directory
out_files = [filename for filename in os.listdir(script_dir) if filename.endswith('.out')]

# Reference values for chemical shifts
reference_values = {
    'C': 52.5022,
    'H': 25.6831
}

shift =[]
name=[]
file_name=[]
# Process each .out file
for out_file in out_files:
    file_path = os.path.join(script_dir, out_file)
    
    print("For output file : ", out_file)
    
    # Open the file for reading
    with open(file_path, 'r') as file:
        data = file.read()

    # Find all matches of atom information using regular expressions
    matches = re.findall(r'Atom:\s+(\d+)\s+(\w+)\s+.*?isotropic\s+=\s+([\d.-]+)', data, re.DOTALL)

    # Iterate over the matches and calculate the chemical shift

    for match in matches:
        atom_number = match[0]
        atom_name = match[1]
        isotropic_value = float(match[2])
        if atom_name in reference_values:
            reference_value = reference_values[atom_name]
            chemical_shift = reference_value - isotropic_value
            file_name.append(out_file)
            shift.append(chemical_shift)
            name.append(atom_name)
            print(f'Atom {atom_number} {atom_name}: chemical shift = {chemical_shift:.4f}')

df = pd.DataFrame({'File':file_name,'Atom_Name':name,'Chemical_Shift':shift})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1',index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.close()

