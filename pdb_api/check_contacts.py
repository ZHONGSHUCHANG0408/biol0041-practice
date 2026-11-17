import csv
import math
from pathlib import Path
import gemmi

with open("pdb_pilot_10_proteins.csv", newline="") as f:
    candidates = list(csv.DictReader(f))

results = []

for row in candidates:
    pdb_id = row["PDB ID"]
    ligand_id = row["Ligand ID"]
    path = Path("recent_structures") / f"{pdb_id}.cif"

    try:
        block = gemmi.cif.read_file(str(path)).sole_block()

        protein_ids = {
            r[0] for r in block.find(
                "_entity_poly.", ["entity_id", "type"]
            )
            if "polypeptide" in r[1].lower()
        }

        atoms = block.find("_atom_site.", [
            "label_entity_id", "label_comp_id",
            "type_symbol", "Cartn_x", "Cartn_y",
            "Cartn_z", "pdbx_PDB_model_num"
        ])

        protein_atoms = []
        ligand_atoms = []
        first_model = None

        for atom in atoms:
            if first_model is None:
                first_model = atom[6]

            if atom[6] != first_model:
                continue

            if atom[2].upper() in ("H", "D"):
                continue

            xyz = tuple(float(atom[i]) for i in (3, 4, 5))

            if atom[0] in protein_ids:
                protein_atoms.append(xyz)
            elif atom[1] == ligand_id:
                ligand_atoms.append(xyz)

        if protein_atoms and ligand_atoms:
            minimum = min(
                math.dist(a, b)
                for a in ligand_atoms
                for b in protein_atoms
            )
            distance = round(minimum, 2)
            status = (
                "Contact within 4 A - review"
                if minimum <= 4
                else "No contact within 4 A - review"
            )
        else:
            distance = ""
            status = "Missing protein or ligand atoms"

        row["Minimum Distance (A)"] = distance
        row["Contact Status"] = status

        print(pdb_id, ligand_id, distance, status)

    except Exception as e:
        row["Minimum Distance (A)"] = ""
        row["Contact Status"] = f"Error: {e}"
        print(pdb_id, "ERROR:", e)

    results.append(row)

with open("pdb_pilot_10_contacts.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\nSaved to pdb_pilot_10_contacts.csv")
