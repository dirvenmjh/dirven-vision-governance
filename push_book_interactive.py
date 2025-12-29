#!/usr/bin/env python3
"""Interactive book push to GitHub - prompts for token"""

import os
import sys
import requests
import base64
from pathlib import Path

print("\n" + "="*70)
print("PUSH BOOK TO GITHUB")
print("="*70)
print("\nUsername: dirvenmjh")
print("\nYou need a GitHub Personal Access Token with 'repo' scope.")
print("Create at: https://github.com/settings/tokens")
print()

GITHUB_TOKEN = input("Enter your GitHub token: ").strip()

if not GITHUB_TOKEN:
    print("[ERROR] No token provided")
    sys.exit(1)

GITHUB_USER = "dirvenmjh"
REPO_NAME = "dirven-books"

BASE_URL = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

book_dir = Path("c:/hashtag1/books/dirven's_vision_for_world_governance")

print(f"\n[INFO] Pushing book to GitHub...")
print(f"[INFO] Repository: {GITHUB_USER}/{REPO_NAME}")
print(f"[INFO] Book directory: {book_dir}")

try:
    # Test authentication
    print("\n[INFO] Testing authentication...")
    response = requests.get(f"{BASE_URL}", headers=HEADERS)
    if response.status_code != 200:
        print(f"[ERROR] Authentication failed: {response.json()}")
        sys.exit(1)
    
    print("[OK] Authenticated successfully")
    
    # Upload files
    files_uploaded = 0
    files_failed = 0
    
    print("\n[INFO] Uploading files...")
    
    for file_path in sorted(book_dir.rglob('*')):
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
                files_failed += 1
                print(f"  [ERROR] {relative_path}: {response.json()}")
    
    print(f"\n[OK] Uploaded {files_uploaded} files!")
    if files_failed > 0:
        print(f"[WARNING] {files_failed} files failed")
    
    print(f"\n[INFO] Your book is now at:")
    print(f"  https://github.com/{GITHUB_USER}/{REPO_NAME}")
    
    print(f"\n[OK] PUSH COMPLETE!")
    
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)
