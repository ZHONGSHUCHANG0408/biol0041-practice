
import requests

url = "https://search.rcsb.org/rcsbsearch/v2/query"

query = {
    "query": {
        "type": "terminal",
        "service": "text",
        "parameters": {
            "attribute": "rcsb_accession_info.initial_release_date",
            "operator": "greater_or_equal",
            "value": "2024-01-01"
        }
    },
    "return_type": "entry",
    "request_options": {
        "paginate": {
            "start": 0,
            "rows": 5
        }
    }
}

response = requests.post(url, json=query, timeout=60)
response.raise_for_status()

data = response.json()

print("Total PDB structures:", data["total_count"])

for result in data["result_set"]:
    print(result["identifier"])

from pathlib import Path

folder = Path("recent_structures")
folder.mkdir(exist_ok=True)

for result in data["result_set"]:
    pdb_id = result["identifier"]
    download_url = f"https://files.rcsb.org/download/{pdb_id}.cif"

    response = requests.get(download_url, timeout=60)
    response.raise_for_status()

    filename = folder / f"{pdb_id}.cif"
    filename.write_bytes(response.content)

    print(f"Downloaded: {pdb_id}.cif")

print("All 5 structures downloaded!")
