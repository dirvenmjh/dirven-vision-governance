#!/usr/bin/env python3
"""
Automated GitHub repository creation and push
Usage: python push_to_github_auto.py <username> <token> [repo_name]
"""

import subprocess
import json
import sys
import urllib.request
import urllib.error

def run_command(cmd, cwd=None):
    """Run shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def create_repo_with_api(token, repo_name, description):
    """Create GitHub repo using API"""
    
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DirvenVision"
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
            result = json.loads(response.read().decode('utf-8'))
            return True, result
    except urllib.error.HTTPError as e:
        error = json.loads(e.read().decode('utf-8'))
        return False, error

def main():
    if len(sys.argv) < 3:
        print("Usage: python push_to_github_auto.py <username> <token> [repo_name]")
        print()
        print("Example:")
        print("  python push_to_github_auto.py dirvenmjh ghp_xxxxx")
        print()
        print("Get token at: https://github.com/settings/tokens/new")
        sys.exit(1)
    
    username = sys.argv[1]
    token = sys.argv[2]
    repo_name = sys.argv[3] if len(sys.argv) > 3 else "dirven-vision-governance"
    
    print("=" * 60)
    print("📚 Dirven's Vision for World Governance")
    print("=" * 60)
    print()
    print(f"Username: {username}")
    print(f"Repository: {repo_name}")
    print(f"Access Level: Public (Free to read)")
    print()
    
    description = "Dirven's Vision for World Governance - A comprehensive framework for transparent, distributed, and democratic global systems"
    
    # Create repo
    print("🔄 Step 1: Creating repository on GitHub...")
    success, result = create_repo_with_api(token, repo_name, description)
    
    if not success:
        print(f"❌ Failed to create repository")
        error_msg = result.get('message', 'Unknown error')
        print(f"Error: {error_msg}")
        if 'errors' in result:
            for error in result['errors']:
                print(f"  - {error.get('message', str(error))}")
        print()
        print("Troubleshooting:")
        print("  - Token expired? Create new one: https://github.com/settings/tokens/new")
        print("  - Repo exists? Use different name or delete it first")
        print("  - No internet? Check connection")
        sys.exit(1)
    
    print("   ✅ Repository created")
    print()
    
    # Push code
    print("🔄 Step 2: Pushing code to GitHub...")
    cwd = "c:/hashtag1"
    
    # Remove old remote if exists
    run_command("git remote remove origin", cwd)
    
    # Add new remote with token authentication
    repo_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    code, out, err = run_command(f'git remote add origin "{repo_url}"', cwd)
    if code != 0:
        print(f"   ❌ Failed to configure git")
        print(f"   Error: {err}")
        sys.exit(1)
    
    # Push
    code, out, err = run_command("git push -u origin main", cwd)
    if code != 0:
        print(f"   ❌ Failed to push code")
        print(f"   Error: {err}")
        sys.exit(1)
    
    print("   ✅ Code pushed successfully")
    print()
    
    # Success!
    print("=" * 60)
    print("✅ SUCCESS!")
    print("=" * 60)
    print()
    print("📖 Your book is live at:")
    print(f"   https://github.com/{username}/{repo_name}")
    print()
    print("📊 What's included:")
    print("   ✅ Complete README (5,000+ words)")
    print("   ✅ 35 full chapters")
    print("   ✅ Author introduction")
    print("   ✅ Table of contents")
    print("   ✅ Contributing guidelines")
    print()
    print("🔗 Next steps:")
    print(f"   1. Open: https://github.com/{username}/{repo_name}")
    print("   2. Share the link")
    print("   3. (Optional) Enable GitHub Pages for a website")
    print()
    print("🎉 Your governance vision is now public!")
    print()

if __name__ == "__main__":
    main()
