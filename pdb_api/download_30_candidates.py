
import requests

url = "https://search.rcsb.org/rcsbsearch/v2/query"

def condition(attribute, operator, value):
    return {
        "type": "terminal",
        "service": "text",
        "parameters": {
            "attribute": attribute,
            "operator": operator,
            "value": value
        }
    }

query = {
    "query": {
        "type": "group",
        "logical_operator": "and",
        "nodes": [
            condition(
                "rcsb_accession_info.initial_release_date",
                "greater_or_equal",
                "2024-01-01"
            ),
            condition(
                "rcsb_entry_info.polymer_entity_count_protein",
                "greater",
                0
            ),
            condition(
                "rcsb_entry_info.nonpolymer_entity_count",
                "greater",
                0
            )
        ]
    },
    "return_type": "entry",
    "request_options": {
        "paginate": {"start": 0, "rows": 30}
    }
}

response = requests.post(url, json=query, timeout=60)
response.raise_for_status()

data = response.json()

print("Total matching structures:", data["total_count"])
print("\nFirst 10 PDB IDs:")

for item in data["result_set"]:
    print(item["identifier"])


from pathlib import Path

folder = Path("recent_structures")
folder.mkdir(exist_ok=True)

for item in data["result_set"]:
    pdb_id = item["identifier"]
    filename = folder / f"{pdb_id}.cif"

    if filename.exists():
        continue

    try:
        url = f"https://files.rcsb.org/download/{pdb_id}.cif"
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        filename.write_bytes(r.content)
        print("Downloaded:", pdb_id)
    except requests.RequestException as e:
        print("Failed:", pdb_id, e)

print("Download step finished.")
