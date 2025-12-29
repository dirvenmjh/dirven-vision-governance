#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import sys

# Fix encoding
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000"

# Create first book
book_data = {
    "title": "Dirven's Vision for World Governance",
    "author": "Dr. Richard (Marinus Jacobus Hendricus) Dirven",
    "description": "A comprehensive guide to transparent, democratic governance systems, prediction markets, and the intersection of technology and human freedom. Founded on principles of merit-based systems, algorithmic transparency, and distributed intelligence."
}

try:
    print("Creating book...")
    response = requests.post(f"{BASE_URL}/api/book/create", json=book_data, timeout=5)
    result = response.json()
    book_id = result.get('book_id')
    
    print("\n[OK] Book created successfully!")
    print(f"  Title: {book_data['title']}")
    print(f"  ID: {book_id}")
    print("\nIn web UI (http://localhost:5000):")
    print("1. Select book from dropdown")
    print("2. Add chapters")
    print("3. Write in Markdown")
    print("4. Upload images")
    print("5. Push to GitHub")
    
except Exception as e:
    print(f"[ERROR] {e}")
    print("\nMake sure Flask app is running:")
    print("  python book_app_web.py")
