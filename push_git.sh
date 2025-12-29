#!/bin/bash
cd "c:/hashtag1/books/dirven's_vision_for_world_governance"

# Remove old remote
git remote remove origin 2>/dev/null || true

# Add new remote
git remote add origin https://github.com/dirvenmjh/dirven-books.git

# Rename branch to main
git branch -M main

# Configure git
git config user.name "Dr. Richard Dirven"
git config user.email "author@dirven.com"

echo "Pushing to GitHub..."
git push -u origin main
