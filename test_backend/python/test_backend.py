import requests
import json
from pprint import pprint

filters = [
    {"key": "name", "op": "contains", "value": "John"},
    {"key": "status", "op": "eq", "value": "Active"}
]

response = requests.post(
    'http://localhost:5000/api/users',
    json=filters,
    params={'page': 1, 'per_page': 10, 'sort_by': 'name', 'order': 'asc'}
)

pprint(json.loads(response.content),indent=1)