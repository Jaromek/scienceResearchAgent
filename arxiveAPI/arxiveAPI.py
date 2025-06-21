import requests
import json

response = requests.get("http://export.arxiv.org/api/query")
print(response.status_code)