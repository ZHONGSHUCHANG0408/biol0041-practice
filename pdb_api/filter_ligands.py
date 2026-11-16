
import requests
import csv
from pathlib import Path

folder = Path("recent_structures")

# Common ions and crystallization additives
exclude = {
    "HOH", "CA", "MG", "ZN", "K",
    "SO4", "CL", "NA", "EDO", "GOL",
    "PEG", "ACT"
}

results = []

for file in sorted(folder.glob("*.cif")):
    pdb_id = file.stem

    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    data = requests.get(url, timeout=30)
    data.raise_for_status()

    entity_ids = data.json().get(
        "rcsb_entry_container_identifiers", {}
    ).get("non_polymer_entity_ids", [])

    for entity_id in entity_ids:
        url = (
            f"https://data.rcsb.org/rest/v1/core/"
            f"nonpolymer_entity/{pdb_id}/{entity_id}"
        )

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        ligand = response.json().get("pdbx_entity_nonpoly", {})
        code = ligand.get("comp_id", "")
        name = ligand.get("name", "")

        if code in exclude:
            status = "Exclude as target ligand"
        else:
            status = "Review candidate"

        results.append([pdb_id, code, name, status])

with open("ligand_screening.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["PDB ID", "Ligand ID", "Name", "Status"])
    writer.writerows(results)

print("Screening completed!")
print("Results saved to ligand_screening.csv")

