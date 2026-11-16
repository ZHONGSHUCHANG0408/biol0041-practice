
import requests

pdb_id = "1HSG"

url = f"https://files.rcsb.org/download/{pdb_id}.cif"

response = requests.get(url, timeout=30)
response.raise_for_status()

with open(f"{pdb_id}.cif", "wb") as file:
    file.write(response.content)

print(f"Successfully downloaded {pdb_id}.cif")

