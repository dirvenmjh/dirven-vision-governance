#!/usr/bin/env python3
"""
Dirven's Book Authoring System
Multi-book template with image/drawing support and GitHub integration
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)


class BookAuthor:
    """Book authoring and management system"""
    
    def __init__(self, github_token: str = None, github_repo: str = None):
        self.github_token = github_token
        self.github_repo = github_repo
        self.books_dir = Path('books')
        self.books_dir.mkdir(exist_ok=True)
        self.config_file = self.books_dir / 'books_config.json'
        self.load_config()
    
    def load_config(self):
        """Load books configuration"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                self.config = json.load(f)
        else:
            self.config = {'books': [], 'github': {'repo': None, 'token': None}}
    
    def save_config(self):
        """Save books configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def create_book(self, title: str, author: str, description: str) -> str:
        """Create new book from template"""
        book_id = title.lower().replace(' ', '_')
        book_dir = self.books_dir / book_id
        book_dir.mkdir(exist_ok=True)
        
        # Create directories
        (book_dir / 'chapters').mkdir(exist_ok=True)
        (book_dir / 'images').mkdir(exist_ok=True)
        (book_dir / 'exports').mkdir(exist_ok=True)
        
        # Create book metadata
        metadata = {
            'title': title,
            'author': author,
            'description': description,
            'created': datetime.now().isoformat(),
            'chapters': [],
            'chapters_dir': str(book_dir / 'chapters'),
            'images_dir': str(book_dir / 'images'),
        }
        
        with open(book_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Create template chapter
        self.create_chapter(book_id, 'Introduction', self.get_template_chapter())
        
        # Add to config
        self.config['books'].append({
            'id': book_id,
            'title': title,
            'path': str(book_dir),
            'created': datetime.now().isoformat()
        })
        self.save_config()
        
        logger.info(f"Created book: {title} ({book_id})")
        return book_id
    
    def get_template_chapter(self) -> str:
        """Get template chapter"""
        return """# Chapter Title

## Section 1
Write your content here.

## Section 2
You can include:
- Bullet points
- **Bold text**
- *Italic text*
- [Links](https://example.com)

### Images
Use: ![Description](../images/filename.jpg)

### Subsections
Continue organizing your content.

---
[Back to Contents](#toc) | [Next Chapter](#next)
"""
    
    def create_chapter(self, book_id: str, title: str, content: str = None) -> str:
        """Add chapter to book"""
        book_dir = self.books_dir / book_id
        
        if not book_dir.exists():
            logger.error(f"Book not found: {book_id}")
            return None
        
        # Load metadata
        with open(book_dir / 'metadata.json') as f:
            metadata = json.load(f)
        
        # Create chapter file
        chapter_id = title.lower().replace(' ', '_')
        chapter_file = book_dir / 'chapters' / f'{len(metadata["chapters"]) + 1:02d}_{chapter_id}.md'
        
        if content is None:
            content = self.get_template_chapter()
        
        with open(chapter_file, 'w') as f:
            f.write(f"# {title}\n\n{content}")
        
        metadata['chapters'].append({
            'id': chapter_id,
            'title': title,
            'file': chapter_file.name,
            'created': datetime.now().isoformat()
        })
        
        with open(book_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Created chapter: {title}")
        return str(chapter_file)
    
    def add_image(self, book_id: str, image_path: str) -> str:
        """Add image to book"""
        book_dir = self.books_dir / book_id
        images_dir = book_dir / 'images'
        
        src = Path(image_path)
        if not src.exists():
            logger.error(f"Image not found: {image_path}")
            return None
        
        dst = images_dir / src.name
        import shutil
        shutil.copy(src, dst)
        
        logger.info(f"Added image: {src.name}")
        return str(dst)
    
    def build_book(self, book_id: str, output_format: str = 'html') -> str:
        """Build book to output format"""
        book_dir = self.books_dir / book_id
        exports_dir = book_dir / 'exports'
        
        with open(book_dir / 'metadata.json') as f:
            metadata = json.load(f)
        
        # Combine all chapters
        full_content = f"# {metadata['title']}\n\nBy {metadata['author']}\n\n"
        full_content += f"{metadata['description']}\n\n---\n\n"
        
        for chapter in metadata['chapters']:
            chapter_file = book_dir / 'chapters' / chapter['file']
            with open(chapter_file) as f:
                full_content += f.read() + "\n\n---\n\n"
        
        # Save combined markdown
        combined_file = exports_dir / f"{book_id}_combined.md"
        with open(combined_file, 'w') as f:
            f.write(full_content)
        
        logger.info(f"Built book: {metadata['title']}")
        return str(combined_file)
    
    def setup_github(self, token: str, repo: str):
        """Setup GitHub integration"""
        self.github_token = token
        self.github_repo = repo
        
        self.config['github'] = {
            'repo': repo,
            'token': '***' if token else None
        }
        self.save_config()
        
        logger.info(f"GitHub configured: {repo}")
    
    def push_to_github(self, book_id: str, message: str = None):
        """Push book to GitHub"""
        if not self.github_repo:
            logger.error("GitHub not configured")
            return False
        
        book_dir = self.books_dir / book_id
        
        try:
            # Initialize git in book dir if needed
            if not (book_dir / '.git').exists():
                os.chdir(book_dir)
                subprocess.run(['git', 'init'], check=True, capture_output=True)
                subprocess.run(['git', 'config', 'user.name', 'BookAuthor'], check=True, capture_output=True)
                subprocess.run(['git', 'config', 'user.email', 'author@dirven.com'], check=True, capture_output=True)
            
            os.chdir(book_dir)
            
            # Add all files
            subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
            
            # Commit
            commit_msg = message or f"Update book: {datetime.now().isoformat()}"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
            
            logger.info(f"Pushed to GitHub: {self.github_repo}")
            return True
        
        except Exception as e:
            logger.error(f"GitHub push failed: {e}")
            return False
    
    def list_books(self):
        """List all books"""
        logger.info("Your Books:")
        for book in self.config['books']:
            logger.info(f"  - {book['title']} ({book['id']})")
        return self.config['books']


def main():
    print("=" * 70)
    print("DIRVEN'S BOOK AUTHORING SYSTEM")
    print("=" * 70)
    
    # Check for GitHub setup
    github_token = os.getenv('GITHUB_TOKEN')
    github_repo = os.getenv('GITHUB_REPO')
    
    if not github_token or not github_repo:
        print("\n⚠️  GitHub Integration Not Configured")
        print("\nTo connect your GitHub repo:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Create a new token with 'repo' scope")
        print("3. Set environment variables:")
        print("   - GITHUB_TOKEN=your_token_here")
        print("   - GITHUB_REPO=username/repo_name")
        print("\nOr run: python book_authoring_app.py --setup-github")
    
    author = BookAuthor(github_token, github_repo)
    
    # Example: Create new book
    if not author.config['books']:
        print("\nCreating your first book...")
        book_id = author.create_book(
            title="Dirven's Vision for World Governance",
            author="Dr. Richard Dirven",
            description="A comprehensive guide to transparent, democratic governance systems"
        )
        
        # Add chapters
        author.create_chapter(book_id, "Chapter 1: The Crisis of Current Systems")
        author.create_chapter(book_id, "Chapter 2: Dirven's Democrats Framework")
        author.create_chapter(book_id, "Chapter 3: Implementation Strategy")
        
        # Build book
        author.build_book(book_id, 'html')
    
    # List books
    author.list_books()
    
    print("\n" + "=" * 70)
    print("GitHub Configuration Status:")
    if github_token and github_repo:
        print(f"✓ Connected to: {github_repo}")
    else:
        print("✗ Not configured. Run: python book_authoring_app.py --setup-github")
    print("=" * 70)


if __name__ == '__main__':
    main()
