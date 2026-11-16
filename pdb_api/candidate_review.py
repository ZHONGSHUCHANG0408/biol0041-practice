
import csv
import requests

candidates = []

with open("ligand_screening.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if row["Status"] != "Review candidate":
            continue

        pdb_id = row["PDB ID"]

        url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        release_date = data["rcsb_accession_info"]["initial_release_date"][:10]

        candidates.append([
            pdb_id,
            row["Ligand ID"],
            row["Name"],
            release_date,
            f"https://www.rcsb.org/structure/{pdb_id}"
        ])

with open("candidate_review.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "PDB ID", "Ligand ID", "Ligand Name",
        "Release Date", "RCSB Link"
    ])
    writer.writerows(candidates)

print(f"Found {len(candidates)} candidate entries.")
print("Saved to candidate_review.csv")

