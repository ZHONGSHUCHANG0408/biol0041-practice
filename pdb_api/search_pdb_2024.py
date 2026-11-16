
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

