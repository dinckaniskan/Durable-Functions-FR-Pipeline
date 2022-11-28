import requests
import time

post_url = 'http://localhost:7071/api/orchestrators/ExtractCertificate'

# sas_token = 'sv=2021-06-08&ss=b&srt=sco&sp=rtf&se=2023-01-01T07:38:50Z&st=2022-11-20T23:38:50Z&spr=https&sig=GGNWi0px8TbYKzCguHCMupuMLTW6Thpz9UIGURhah%2F0%3D'

# sp=r&st=2022-11-20T22:52:36Z&se=2022-11-27T06:52:36Z&spr=https&sv=2021-06-08&sr=b&sig=wvJZqnkVAnJONt8KsO1vPJLtQ30X4SwvDK8bx4mmFbo%3D

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