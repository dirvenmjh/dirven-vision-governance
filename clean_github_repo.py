#!/usr/bin/env python3
"""Clean old files from GitHub repository"""

import requests
import sys
from pathlib import Path

print("\n" + "="*70)
print("CLEAN GITHUB REPOSITORY")
print("="*70)

GITHUB_TOKEN = input("\nEnter your GitHub token: ").strip()

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

# Files to delete from GitHub (keep only book content & images)
FILES_TO_DELETE = [
    "dirven's_vision_for_world_governance/PUSH_TO_GITHUB.bat",
    "dirven's_vision_for_world_governance/.git",
    "dirven's_vision_for_world_governance/exports",
]

print(f"\n[INFO] Cleaning repository: {GITHUB_USER}/{REPO_NAME}")

try:
    # Test authentication
    response = requests.get(f"{BASE_URL}", headers=HEADERS)
    if response.status_code != 200:
        print(f"[ERROR] Authentication failed: {response.json()}")
        sys.exit(1)
    
    print("[OK] Authenticated")
    
    files_deleted = 0
    
    # Delete each file
    for file_path in FILES_TO_DELETE:
        delete_url = f"{BASE_URL}/contents/{file_path}"
        
        # Get file SHA first
        get_response = requests.get(delete_url, headers=HEADERS)
        
        if get_response.status_code == 200:
            file_sha = get_response.json()["sha"]
            
            # Delete file
            delete_data = {
                "message": f"Remove: {file_path.split('/')[-1]}",
                "sha": file_sha
            }
            
            delete_response = requests.delete(delete_url, headers=HEADERS, json=delete_data)
            
            if delete_response.status_code in [200, 204]:
                files_deleted += 1
                print(f"  [OK] Deleted: {file_path}")
            else:
                print(f"  [INFO] Could not delete: {file_path} (status: {delete_response.status_code})")
        else:
            print(f"  [INFO] File not found: {file_path}")
    
    print(f"\n[OK] Cleanup complete! Deleted {files_deleted} files")
    print(f"Repository: https://github.com/{GITHUB_USER}/{REPO_NAME}")
    
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)
