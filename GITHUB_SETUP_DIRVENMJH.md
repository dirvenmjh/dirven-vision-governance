# GitHub Connection Setup for dirvenmjh

Personal GitHub integration for Dirven's Book Authoring System.

## Step 1: Create Repository

1. Go to: https://github.com/new
2. Fill in:
   - **Repository name**: `dirven-books`
   - **Description**: "Dirven's published books, research, and writings"
   - **Visibility**: Public (so your books are accessible worldwide)
   - **Initialize with README**: Yes
3. Click "Create repository"

Your repo will be: `https://github.com/dirvenmjh/dirven-books`

## Step 2: Generate GitHub Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Fill in:
   - **Token name**: `dirven-books-app`
   - **Expiration**: No expiration (or 90 days if you prefer)
   - **Scopes**: Check:
     - ✓ `repo` (Full control of private repositories)
     - ✓ `workflow` (Update GitHub Action workflows)
4. Click "Generate token"
5. **Copy the token** (you'll only see it once!)
6. Store safely - you'll need it in the next step

Example token format: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Step 3: Connect in Book App

Run the web app:
```bash
python book_app_web.py
```

Open: http://localhost:5000

In the "GitHub Integration" section:
- **GitHub Token**: Paste your token from Step 2
- **Repository**: `dirvenmjh/dirven-books`
- Click "Connect GitHub"

Status should show: ✓ Connected to: dirvenmjh/dirven-books

## Step 4: Start Writing!

1. Create new book
2. Add chapters
3. Upload images
4. Click "Push to GitHub" to sync

All your books automatically sync to:
https://github.com/dirvenmjh/dirven-books

## Your Book Repository Structure

```
https://github.com/dirvenmjh/dirven-books
└── books/
    ├── dirven_vision_governance/
    │   ├── chapters/
    │   ├── images/
    │   └── metadata.json
    ├── [next-book]/
    └── books_config.json
```

## Public Access

Once pushed to GitHub, your books are viewable at:

**Raw Markdown:**
https://github.com/dirvenmjh/dirven-books/blob/main/books/[book-id]/chapters/

**GitHub Pages (if enabled):**
1. Go to repo Settings → Pages
2. Set source to `main` branch
3. Your books become: https://dirvenmjh.github.io/dirven-books/

## Verify Connection

After connecting in the app, you can verify on GitHub:

1. Go to: https://github.com/dirvenmjh/dirven-books
2. You should see commits appearing as you push books
3. Click on commits to see your book changes

## Token Security

⚠️ **Important:**
- Never share your token publicly
- Don't commit it to repositories
- If exposed, regenerate immediately at https://github.com/settings/tokens
- The app stores it locally only, never transmits elsewhere

## If You Don't Have a GitHub Account

1. Go to: https://github.com/signup
2. Create account: `dirvenmjh` (your username)
3. Verify email
4. Then follow steps above

## Quick Commands (Optional)

If you prefer command-line instead of web UI:

```bash
cd c:/hashtag1/books/dirven_vision_governance

git init
git config user.name "Richard Dirven"
git config user.email "your@email.com"

git add .
git commit -m "Initial commit: Dirven's Vision for World Governance"

git remote add origin https://github.com/dirvenmjh/dirven-books.git
git branch -M main
git push -u origin main
```

## What Gets Synced?

✓ All chapters (Markdown)
✓ All images
✓ Book metadata
✓ Build outputs (HTML)
✗ `.git` directories (system files)

## Support

If token doesn't work:
1. Verify token hasn't expired
2. Check repository name spelling: `dirvenmjh/dirven-books`
3. Regenerate token if needed
4. Restart app and reconnect

---

**Your GitHub Profile:** https://github.com/dirvenmjh  
**Your Books Repo:** https://github.com/dirvenmjh/dirven-books  
**Setup Time:** ~5 minutes

Ready to write and publish your books!
