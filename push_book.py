#!/usr/bin/env python3
import requests
import sys

BASE_URL = "http://localhost:5000"

book_id = "dirven's_vision_for_world_governance"

print(f"Pushing book to GitHub: {book_id}")

try:
    response = requests.post(f"{BASE_URL}/api/book/{book_id}/push", timeout=30)
    result = response.json()
    
    if result.get('success'):
        print("[OK] Book pushed to GitHub successfully!")
        print(f"\nView at: https://github.com/dirvenmjh/dirven-books")
    else:
        print("[ERROR] Push failed")
        print(result)
        
except Exception as e:
    print(f"[ERROR] {e}")
    print("\nMake sure:")
    print("1. Flask app is running: python book_app_web.py")
    print("2. GitHub token is set in environment")
    sys.exit(1)
