import requests
import os

token = os.getenv('GITHUB_TOKEN', '[REDACTED:github-pat]')
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

response = requests.get('https://api.github.com/user', headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    user = response.json()
    print(f"User: {user.get('login')}")
    print(f"Name: {user.get('name')}")
    print("Token is valid!")
else:
    print(f"Error: {response.json()}")
