import requests
import time

post_url = 'http://localhost:7071/api/orchestrators/ExtractCertificate'

body = {
    'docs': [
        f"https://frstorageaccount1234.blob.core.windows.net/raw/sample.pdf",
    ]
}

r = requests.post(post_url, json=body).json()

print(r)

get_url = r['statusQueryGetUri']
r = requests.get(get_url).json()

while r['runtimeStatus'] != 'Completed':
    r = requests.get(get_url).json()
    time.sleep(5)

print(r)