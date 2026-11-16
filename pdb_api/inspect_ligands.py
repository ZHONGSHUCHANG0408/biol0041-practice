
from pathlib import Path
import requests

folder = Path("recent_structures")

for file in sorted(folder.glob("*.cif")):
    pdb_id = file.stem
    print(f"\nPDB ID: {pdb_id}")

    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    entity_ids = data.get(
        "rcsb_entry_container_identifiers", {}
    ).get("non_polymer_entity_ids", [])

    if not entity_ids:
        print("No non-polymer entities listed.")
        continue

    for entity_id in entity_ids:
        url = (
            f"https://data.rcsb.org/rest/v1/core/"
            f"nonpolymer_entity/{pdb_id}/{entity_id}"
        )
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        ligand = response.json().get("pdbx_entity_nonpoly", {})
        print(ligand.get("comp_id"), "-", ligand.get("name"))

