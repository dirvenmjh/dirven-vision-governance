#!/usr/bin/env python3
"""Push book to GitHub using REST API"""

import requests
import json
from pathlib import Path
import base64
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("[ERROR] Set GITHUB_TOKEN environment variable")
    exit(1)

GITHUB_USER = "dirvenmjh"
REPO_NAME = "dirven-books"

BASE_URL = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

book_dir = Path("c:/hashtag1/books/dirven's_vision_for_world_governance")

print(f"\n[INFO] Pushing book to GitHub API...")
print(f"[INFO] Repository: {GITHUB_USER}/{REPO_NAME}")

try:
    # Test authentication
    response = requests.get(f"{BASE_URL}", headers=HEADERS)
    if response.status_code != 200:
        print(f"[ERROR] Authentication failed: {response.json()}")
        exit(1)
    
    print("[OK] Authenticated")
    
    # Upload files
    files_uploaded = 0
    
    for file_path in book_dir.rglob('*'):
        if file_path.is_file() and '.git' not in str(file_path):
            relative_path = file_path.relative_to(book_dir.parent)
            
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # Encode content
            encoded_content = base64.b64encode(file_content).decode('utf-8')
            
            # Check if file exists and get SHA
            check_url = f"{BASE_URL}/contents/{relative_path}"
            check_response = requests.get(check_url, headers=HEADERS)
            
            # Prepare data
            data = {
                "message": f"Upload: {file_path.name}",
                "content": encoded_content
            }
            
            # If file exists, add SHA for update
            if check_response.status_code == 200:
                data["sha"] = check_response.json()["sha"]
            
            # Upload to GitHub
            response = requests.put(check_url, headers=HEADERS, json=data)
            
            if response.status_code in [200, 201]:
                files_uploaded += 1
                print(f"  [OK] {relative_path}")
            else:
                print(f"  [ERROR] {relative_path}: {response.json()}")
    
    print(f"\n[OK] Pushed {files_uploaded} files!")
    print(f"\nView at: https://github.com/{GITHUB_USER}/{REPO_NAME}")
    
except Exception as e:
    print(f"[ERROR] {e}")
