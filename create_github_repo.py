#!/usr/bin/env python3
"""Create GitHub repository for Dirven's books"""

import requests
import webbrowser
import time

token = input("GitHub Token: ").strip()

if not token:
    print("[ERROR] No token provided")
    print("\nGo to: https://github.com/settings/tokens")
    print("Create new token with 'repo' scope")
    input("Press Enter to open GitHub...")
    webbrowser.open("https://github.com/settings/tokens")
    exit(1)

print("\nCreating repository: dirven-books")
print("User: dirvenmjh")

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

data = {
    'name': 'dirven-books',
    'description': 'Dirven\'s published books and writings',
    'homepage': 'https://github.com/dirvenmjh/dirven-books',
    'private': False,
    'auto_init': True
}

try:
    response = requests.post('https://api.github.com/user/repos', 
                            headers=headers, json=data)
    
    if response.status_code == 201:
        print("\n[OK] Repository created successfully!")
        print("\nRepository: https://github.com/dirvenmjh/dirven-books")
        print("\nOpening in browser...")
        time.sleep(2)
        webbrowser.open("https://github.com/dirvenmjh/dirven-books")
        print("\nNow run: python push_via_api.py")
    else:
        print(f"\n[ERROR] {response.status_code}: {response.json()}")
        
except Exception as e:
    print(f"[ERROR] {e}")
