# Dirven's Book Authoring System

Complete multi-book publishing platform with GitHub integration, image support, and Markdown editing.

**Author**: Dr. Richard (Marinus Jacobus Hendricus) Dirven  
**GitHub**: https://github.com/dirvenmjh  
**Books Repository**: https://github.com/dirvenmjh/dirven-books  

---

## What You Get

✓ **Web-based book editor** - Write in Markdown with live interface  
✓ **Multi-book management** - Manage entire series in one system  
✓ **Image/drawing support** - Upload diagrams, photos, sketches  
✓ **Auto-save** - Never lose your work  
✓ **GitHub sync** - One-click publish to GitHub  
✓ **HTML export** - Build standalone books  
✓ **Public sharing** - Share your work with the world  

---

## Quick Start (5 minutes)

### 1. Prerequisites
```bash
pip install flask
```

### 2. Get GitHub Token
- Go to: https://github.com/settings/tokens
- Create new token (classic)
- Check `repo` scope
- Copy token

### 3. Create GitHub Repo
- Go to: https://github.com/new
- Name: `dirven-books`
- Visibility: Public
- Create it

### 4. Run the App
```bash
python book_app_web.py
```
Opens: http://localhost:5000

### 5. Connect GitHub
- In web UI, enter:
  - GitHub Token (from step 2)
  - Repository: `dirvenmjh/dirven-books`
- Click "Connect GitHub"

### 6. Start Writing!
- Create book
- Add chapters
- Write in Markdown
- Upload images
- Push to GitHub

---

## Files

| File | Purpose |
|------|---------|
| `book_authoring_app.py` | Core system (no UI) |
| `book_app_web.py` | Web interface (Flask) |
| `START_BOOK_APP.bat` | Quick launcher |
| `GITHUB_SETUP_DIRVENMJH.md` | Step-by-step GitHub setup |
| `BOOK_APP_SETUP.md` | Complete documentation |
| `books/` | Your books directory |

---

## Your First Book

The system automatically creates your first book:

**Title**: Dirven's Vision for World Governance  
**Author**: Dr. Richard Dirven  
**Status**: Ready to edit and publish

Edit in web UI, push to: https://github.com/dirvenmjh/dirven-books

---

## Book Series Ideas

Plan your complete book collection:

1. **"Dirven's Vision for World Governance"** ← Start here
2. "Transparent Democracy: Technical Foundations"
3. "Numerai and Prediction Markets as Governance Models"
4. "Counter-Intelligence and Personal Freedom"
5. "Building Global Business Systems"
6. "Cognitive Enhancement and Rational Policy"

Each book in same GitHub repo, manageable from one interface.

---

## Markdown Cheatsheet

```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold** *Italic*

- Bullet
- List

1. Numbered
2. List

[Link](https://example.com)
![Image](../images/filename.jpg)

> Quote

\`\`\`python
code
\`\`\`
```

---

## Publishing Workflow

```
Write in Web UI
    ↓
Save Chapter
    ↓
Upload Images
    ↓
Click "Push to GitHub"
    ↓
Auto-commit to: github.com/dirvenmjh/dirven-books
    ↓
Public access to your books
```

---

## GitHub Integration Details

**What syncs:**
- All chapters (Markdown)
- All images
- Book metadata
- Built HTML files

**Where it goes:**
```
https://github.com/dirvenmjh/dirven-books/
└── books/
    └── [book-id]/
        ├── chapters/
        ├── images/
        └── metadata.json
```

**Public access:**
```
Raw files: github.com/dirvenmjh/dirven-books
Pages: dirvenmjh.github.io/dirven-books (if enabled)
```

---

## Features in Detail

### Create Multiple Books
Each book has:
- Own directory
- Own metadata
- Own chapters
- Own images
- Independent git history

### Chapter Management
- Add chapters one at a time
- Edit existing chapters
- Organize chronologically
- Add sections and subsections

### Image Support
- Upload PNG, JPG, GIF, SVG
- Auto-organized in book's images folder
- Reference in Markdown: `![](../images/filename.jpg)`
- Support for diagrams, drawings, photos

### GitHub Workflow
- Automatic commits on push
- Full version history
- Track changes over time
- Collaborate (with permission)
- Public visibility

### Export Formats
- **Markdown** - Raw chapters
- **HTML** - Standalone viewing
- **GitHub** - Web-accessible

---

## Example Books to Create

### Academic/Technical
- "Numerai: A Case Study in Distributed Intelligence"
- "Cryptocurrency Governance: Lessons for Democracy"
- "Data Science Competition Rankings: What They Mean"

### Personal/Leadership
- "Building Global Teams: Lessons from 100+ Employees"
- "From Coding to Command: A Journey in Tech Leadership"
- "Family, Business, and Social Responsibility"

### Advocacy
- "The V2K Crisis: Protecting Against Neural Weapons"
- "Transparent Governance: Why It Matters"
- "Rational Drug Policy: Evidence Over Ideology"

### Series
- "Dirven's Vision" (multi-volume set)
- "Global Democracy Series" (collaborative works)
- "Technical Foundations" (for engineers)

---

## Troubleshooting

**Web UI not loading?**
- Check port 5000 is free
- Restart: `python book_app_web.py`

**GitHub push fails?**
- Verify token is valid
- Check repo exists: https://github.com/dirvenmjh/dirven-books
- Regenerate token if expired

**Images not showing?**
- Verify file is in `books/[book-id]/images/`
- Check Markdown: `![](../images/filename.jpg)`
- Check filename spelling

**Lost my token?**
- Go to https://github.com/settings/tokens
- Generate new one
- Update in web UI

---

## Advanced Usage

### Command Line Push
```bash
cd books/[book-id]
git add .
git commit -m "Update: [description]"
git push origin main
```

### Enable GitHub Pages
1. Go to repo Settings → Pages
2. Source: main branch
3. Your books become: https://dirvenmjh.github.io/dirven-books/

### Collaborate
1. Go to repo Settings → Collaborators
2. Add GitHub usernames
3. They can push their own books

---

## Next Steps

1. **Read**: `GITHUB_SETUP_DIRVENMJH.md`
2. **Run**: `python book_app_web.py`
3. **Create**: Your first book
4. **Write**: Opening chapter
5. **Push**: To GitHub
6. **Share**: Your GitHub repo URL

---

## Success Criteria

✓ Book app running on http://localhost:5000  
✓ GitHub token connected  
✓ First book created  
✓ Chapter written  
✓ Images uploaded  
✓ Pushed to GitHub successfully  
✓ Viewable at: github.com/dirvenmjh/dirven-books  

---

## Support

- **Documentation**: GITHUB_SETUP_DIRVENMJH.md
- **Setup Guide**: BOOK_APP_SETUP.md
- **Source Code**: book_authoring_app.py, book_app_web.py
- **GitHub Issues**: https://github.com/dirvenmjh/dirven-books/issues

---

**Start publishing your books now!**

```bash
python book_app_web.py
```

Open: http://localhost:5000
