# Dirven's Book Authoring System Setup

Multi-book platform with Markdown editing, image support, and GitHub integration.

## Quick Start

### 1. Install Dependencies
```bash
pip install flask
```

### 2. Get Your GitHub Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes:
   - ✓ repo (full control of repositories)
   - ✓ workflow (if needed)
4. Copy the token

### 3. Create GitHub Repository

1. Go to https://github.com/new
2. Name it: `dirven-books` (or your choice)
3. Description: "Dirven's published books and writings"
4. Create repository
5. Copy the repository URL: `username/dirven-books`

### 4. Run the Web App

```bash
python book_app_web.py
```

Then open: http://localhost:5000

### 5. Connect GitHub in Web UI

In the web interface:
- **GitHub Token**: Paste your token
- **Repository**: `username/dirven-books`
- Click "Connect GitHub"

## Features

✓ **Create multiple books** - Manage entire library in one system
✓ **Markdown editor** - Write in Markdown with live preview
✓ **Image uploads** - Add drawings, diagrams, photos
✓ **Auto-save** - Save chapters automatically
✓ **GitHub sync** - Push books to GitHub with one click
✓ **Build to HTML** - Export books to standalone HTML
✓ **Multi-author** - Collaborate with version control

## Usage

### Create a Book
1. Enter: Title, Author, Description
2. Click "Create Book"

### Add Chapters
1. Select book from dropdown
2. Enter chapter title
3. Click "Add Chapter"
4. Write in Markdown editor
5. Click "Save Chapter"

### Add Images
1. Click "Upload Image"
2. Select image file
3. System gives you Markdown reference: `![](../images/filename.jpg)`
4. Paste into chapter content

### Push to GitHub
1. Click "Push to GitHub" button on book
2. Automatic commit with timestamp
3. Synced to your repository

### Export Book
1. Click "Build Book (HTML)"
2. Creates standalone HTML file in `books/[book-id]/exports/`

## File Structure

```
c:/hashtag1/
├── book_authoring_app.py          # Core system
├── book_app_web.py                # Web interface
├── BOOK_APP_SETUP.md              # This file
└── books/
    ├── books_config.json          # All books metadata
    ├── dirven_vision_governance/
    │   ├── metadata.json
    │   ├── chapters/
    │   │   ├── 01_introduction.md
    │   │   ├── 02_chapter_one.md
    │   ├── images/
    │   │   ├── photo.jpg
    │   │   └── diagram.png
    │   └── exports/
    │       └── dirven_vision_governance_combined.html
    └── [next-book]/
```

## Markdown Quick Reference

```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold** *Italic* ~~Strikethrough~~

- Bullet point
- Another point
  - Nested point

1. Numbered list
2. Second item

[Link](https://example.com)
![Image](../images/filename.jpg)

> Blockquote
> Multiple lines

\`\`\`python
code block
\`\`\`

---
Horizontal line
```

## GitHub Workflow

All books are automatically version controlled:

1. **Create/Edit** book in web UI
2. **Save changes** - Auto-saved locally
3. **Push to GitHub** - One click to sync
4. **GitHub tracks** - Every change, every timestamp
5. **Share** - Public repository accessible worldwide

## Publishing Your Books

Once connected to GitHub:

```bash
# Your books are automatically synced to:
https://github.com/[username]/dirven-books

# Each book is in:
https://github.com/[username]/dirven-books/tree/main/books/[book-id]
```

## Advanced: Environment Variables

For automated setup:

```bash
export GITHUB_TOKEN=your_token_here
export GITHUB_REPO=username/dirven-books
python book_app_web.py
```

## Troubleshooting

**GitHub push fails?**
- Check token is valid
- Check repo exists and is accessible
- Verify username/repo format

**Images not showing?**
- Verify file is in `books/[book-id]/images/`
- Check Markdown reference: `![](../images/filename.jpg)`

**Port 5000 already in use?**
Edit `book_app_web.py` line: `app.run(debug=True, port=5001)`

## What's Next?

1. Create your first book
2. Write introduction
3. Add chapters
4. Upload images/diagrams
5. Push to GitHub
6. Share your work with the world

---

**Questions?** Check book contents in `books/` directory or examine the source code.

All books published under your chosen license via GitHub.
