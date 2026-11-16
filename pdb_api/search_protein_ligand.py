
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
        "paginate": {"start": 0, "rows": 10}
    }
}

response = requests.post(url, json=query, timeout=60)
response.raise_for_status()

data = response.json()

print("Total matching structures:", data["total_count"])
print("\nFirst 10 PDB IDs:")

for item in data["result_set"]:
    print(item["identifier"])

