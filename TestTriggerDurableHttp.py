import requests
import time

post_url = 'https://testingfrapp.azurewebsites.net/api/orchestrators/ExtractCertificate?code=pOFpSCiy55OXj0mRfhwF4ezFDo1p_iS6RIM_meCe4Z3XAzFuBVxzHQ=='

body = {
    'docs': [
        f"https://frstorageaccount1234.blob.core.windows.net/raw/sample.pdf",
    ]
}

r = requests.post(post_url, json=body)

print(r)
print(r.text)

r = r.json()

get_url = r['statusQueryGetUri']
r = requests.get(get_url).json()

while r['runtimeStatus'] != 'Completed':
    r = requests.get(get_url).json()
    time.sleep(5)

print(r)