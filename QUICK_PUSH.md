# Quick Push to GitHub

Your book needs one thing: a GitHub Personal Access Token

## Step 1: Create Personal Access Token

1. Go to: https://github.com/settings/tokens/new
2. Name: `book-push-token`
3. Check: ✅ `repo` (full control of private repositories)
4. Click **Generate token**
5. **Copy the token** (you won't see it again)

## Step 2: Run This Command

Replace `YOUR_TOKEN` with the token you just copied:

```bash
python push_to_github_auto.py dirvenmjh YOUR_TOKEN
```

That's it. The script will:
- Create the repo `dirven-vision-governance` 
- Push all your book content
- Give you the final GitHub URL

## Example

```bash
python push_to_github_auto.py dirvenmjh ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Don't have Python?** Use the manual method below.

---

## Manual Method (No Python)

If you prefer to do it yourself, create the repo at https://github.com/new:

1. **Repository name**: `dirven-vision-governance`
2. **Description**: "Dirven's Vision for World Governance"
3. **Visibility**: Public
4. Click **Create repository**

Then run:
```bash
git remote add origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/dirven-vision-governance.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_TOKEN`.

---

That's all you need!
