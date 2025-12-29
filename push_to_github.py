#!/usr/bin/env python3
"""
Automated GitHub repository creation and push script
Creates a new public repo and pushes the book to it
"""

import subprocess
import json
import os
from datetime import datetime

def run_command(cmd, cwd=None):
    """Run shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def create_repo_with_api(username, token, repo_name, description):
    """Create GitHub repo using API"""
    import urllib.request
    import urllib.error
    
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = json.dumps({
        "name": repo_name,
        "description": description,
        "public": True,
        "auto_init": False
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            return True, result
    except urllib.error.HTTPError as e:
        error = json.loads(e.read())
        return False, error

def main():
    print("=" * 60)
    print("GitHub Repository Setup for Dirven's Vision")
    print("=" * 60)
    print()
    
    # Get GitHub credentials
    print("To create and push your repository, you need:")
    print("1. Your GitHub username")
    print("2. A Personal Access Token (generate at https://github.com/settings/tokens)")
    print()
    
    username = input("GitHub username (e.g., dirvenmjh): ").strip()
    if not username:
        print("❌ Username required")
        return False
    
    token = input("GitHub Personal Access Token: ").strip()
    if not token:
        print("❌ Token required")
        return False
    
    # Create repo name
    timestamp = datetime.now().strftime("%Y%m%d")
    repo_name = "dirven-vision-governance"
    
    print()
    print(f"Creating repository: {repo_name}")
    print(f"GitHub URL: https://github.com/{username}/{repo_name}")
    print()
    
    description = "Dirven's Vision for World Governance - A comprehensive framework for transparent, distributed, and democratic global systems"
    
    # Create repo via API
    print("🔄 Creating repository on GitHub...")
    success, result = create_repo_with_api(username, token, repo_name, description)
    
    if not success:
        print(f"❌ Failed to create repository")
        print(f"Error: {result.get('message', 'Unknown error')}")
        if 'errors' in result:
            for error in result['errors']:
                print(f"  - {error}")
        return False
    
    print("✅ Repository created successfully")
    print()
    
    # Push code
    print("🔄 Configuring git and pushing code...")
    cwd = "c:/hashtag1"
    
    # Remove old remote if exists
    run_command("git remote remove origin", cwd)
    
    # Add new remote
    repo_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    code, out, err = run_command(f'git remote add origin "{repo_url}"', cwd)
    if code != 0:
        print(f"❌ Failed to add remote: {err}")
        return False
    
    # Ensure main branch
    code, out, err = run_command("git branch -M main", cwd)
    
    # Push
    code, out, err = run_command("git push -u origin main", cwd)
    if code != 0:
        print(f"❌ Failed to push: {err}")
        return False
    
    print("✅ Code pushed successfully")
    print()
    
    # Summary
    print("=" * 60)
    print("✅ SUCCESS!")
    print("=" * 60)
    print()
    print(f"Your book is now live at:")
    print(f"📖 https://github.com/{username}/{repo_name}")
    print()
    print("What's included:")
    print("  ✅ Complete README with overview and concepts")
    print("  ✅ All 35 chapters of the book")
    print("  ✅ Table of contents with reading guides")
    print("  ✅ Contributing guidelines")
    print("  ✅ GitHub setup instructions")
    print()
    print("Next steps:")
    print("  1. Visit the GitHub repo")
    print("  2. Share the link with others")
    print("  3. (Optional) Enable GitHub Pages for a website version")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
