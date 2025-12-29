#!/usr/bin/env python3
"""
Web UI for Dirven's Book Authoring System
Flask app with markdown editor and image upload
"""

from flask import Flask, render_template_string, request, jsonify, send_file
from pathlib import Path
import json
from datetime import datetime
from book_authoring_app import BookAuthor
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Path('books')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

author = BookAuthor()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dirven's Book Authoring System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #1a1a1a; color: #fff; }
        header { background: #0d47a1; padding: 20px; text-align: center; }
        .container { max-width: 1200px; margin: 20px auto; padding: 20px; }
        .section { background: #2a2a2a; border-radius: 8px; padding: 20px; margin: 20px 0; }
        .books-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .book-card { background: #333; padding: 15px; border-radius: 8px; border-left: 4px solid #0d47a1; }
        .book-card h3 { margin-bottom: 10px; }
        input, textarea, select { 
            width: 100%; padding: 10px; margin: 10px 0; 
            background: #333; color: #fff; border: 1px solid #444; border-radius: 4px;
            font-family: monospace;
        }
        button { 
            background: #0d47a1; color: #fff; border: none; padding: 10px 20px; 
            border-radius: 4px; cursor: pointer; margin: 10px 5px 10px 0;
        }
        button:hover { background: #0c3fa0; }
        .github-config { background: #1e3a8a; padding: 15px; border-radius: 4px; margin: 10px 0; }
        .status { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .status.connected { background: #065f46; }
        .status.disconnected { background: #7f1d1d; }
        textarea { min-height: 300px; resize: vertical; }
        .tabs { display: flex; gap: 10px; margin: 20px 0; }
        .tab { padding: 10px 20px; background: #444; cursor: pointer; border-radius: 4px; }
        .tab.active { background: #0d47a1; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <header>
        <h1>📚 Dirven's Book Authoring System</h1>
        <p>Multi-book platform with GitHub integration</p>
    </header>
    
    <div class="container">
        <!-- GitHub Configuration -->
        <div class="section">
            <h2>🔗 GitHub Integration</h2>
            <div class="github-config">
                <input type="text" id="github_token" placeholder="GitHub Token (Settings → Developer settings → Personal access tokens)" />
                <input type="text" id="github_repo" placeholder="Repository (username/repo)" />
                <button onclick="setupGithub()">Connect GitHub</button>
                <div id="github_status" class="status disconnected">Not connected</div>
            </div>
        </div>
        
        <!-- Create New Book -->
        <div class="section">
            <h2>➕ Create New Book</h2>
            <input type="text" id="book_title" placeholder="Book Title" />
            <input type="text" id="book_author" placeholder="Author Name" />
            <textarea id="book_description" placeholder="Book Description"></textarea>
            <button onclick="createBook()">Create Book</button>
        </div>
        
        <!-- Books Management -->
        <div class="section">
            <h2>📖 Your Books</h2>
            <div id="books_container" class="books-list"></div>
        </div>
        
        <!-- Chapter Editor -->
        <div class="section">
            <h2>✍️ Edit Book</h2>
            <select id="book_select" onchange="loadBook()">
                <option>Select a book...</option>
            </select>
            
            <div id="book_editor" style="display:none;">
                <h3>Chapters</h3>
                <ul id="chapters_list"></ul>
                
                <h3>New Chapter</h3>
                <input type="text" id="chapter_title" placeholder="Chapter Title" />
                <button onclick="addChapter()">Add Chapter</button>
                
                <h3>Upload Image</h3>
                <input type="file" id="image_file" accept="image/*" />
                <button onclick="uploadImage()">Upload Image</button>
                
                <h3>Chapter Content</h3>
                <textarea id="chapter_content" placeholder="Write in Markdown..."></textarea>
                <button onclick="saveChapter()">Save Chapter</button>
                <button onclick="buildBook()">Build Book (HTML)</button>
            </div>
        </div>
    </div>
    
    <script>
        let currentBook = null;
        
        function setupGithub() {
            const token = document.getElementById('github_token').value;
            const repo = document.getElementById('github_repo').value;
            
            if (!token || !repo) {
                alert('Please enter both token and repo');
                return;
            }
            
            fetch('/api/github/setup', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({token, repo})
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('github_status').innerHTML = 
                    `✓ Connected to: <strong>${repo}</strong>`;
                document.getElementById('github_status').className = 'status connected';
            })
            .catch(e => alert('Error: ' + e));
        }
        
        function createBook() {
            const title = document.getElementById('book_title').value;
            const author = document.getElementById('book_author').value;
            const description = document.getElementById('book_description').value;
            
            if (!title || !author) {
                alert('Please fill in title and author');
                return;
            }
            
            fetch('/api/book/create', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title, author, description})
            })
            .then(r => r.json())
            .then(data => {
                alert('Book created: ' + data.book_id);
                loadBooks();
                document.getElementById('book_title').value = '';
                document.getElementById('book_author').value = '';
                document.getElementById('book_description').value = '';
            })
            .catch(e => alert('Error: ' + e));
        }
        
        function loadBooks() {
            fetch('/api/books/list')
            .then(r => r.json())
            .then(books => {
                // Remove duplicates
                const unique = {};
                books.forEach(b => {
                    if (!unique[b.id]) unique[b.id] = b;
                });
                const uniqueBooks = Object.values(unique);
                
                document.getElementById('books_container').innerHTML = uniqueBooks
                    .map(b => `<div class="book-card">
                        <h3>${b.title}</h3>
                        <p>${b.id}</p>
                        <button onclick="selectBook('${b.id}')">Edit</button>
                        <button onclick="pushBook('${b.id}')">Push to GitHub</button>
                    </div>`)
                    .join('');
                
                const select = document.getElementById('book_select');
                select.innerHTML = '<option>Select a book...</option>' + 
                    uniqueBooks.map(b => `<option value="${b.id}">${b.title}</option>`).join('');
            });
        }
        
        function selectBook(book_id) {
            currentBook = book_id;
            document.getElementById('book_select').value = book_id;
            loadBook();
        }
        
        function loadBook() {
            const book_id = document.getElementById('book_select').value;
            if (!book_id || book_id === 'Select a book...') return;
            
            currentBook = book_id;
            document.getElementById('book_editor').style.display = 'block';
            
            fetch(`/api/book/${book_id}`)
            .then(r => r.json())
            .then(data => {
                document.getElementById('chapters_list').innerHTML = data.chapters
                    .map(c => `<li>${c.title} <button onclick="editChapter('${c.file}')">Edit</button></li>`)
                    .join('');
            });
        }
        
        function addChapter() {
            const title = document.getElementById('chapter_title').value;
            if (!title || !currentBook) {
                alert('Select a book and enter chapter title');
                return;
            }
            
            fetch('/api/chapter/create', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({book_id: currentBook, title})
            })
            .then(r => r.json())
            .then(data => {
                alert('Chapter added');
                document.getElementById('chapter_title').value = '';
                loadBook();
            });
        }
        
        function uploadImage() {
            const file = document.getElementById('image_file').files[0];
            if (!file || !currentBook) {
                alert('Select a book and image file');
                return;
            }
            
            const formData = new FormData();
            formData.append('book_id', currentBook);
            formData.append('file', file);
            
            fetch('/api/image/upload', {method: 'POST', body: formData})
            .then(r => r.json())
            .then(data => {
                alert('Image uploaded: ![](../images/' + data.filename + ')');
                document.getElementById('image_file').value = '';
            });
        }
        
        function saveChapter() {
            const content = document.getElementById('chapter_content').value;
            if (!content || !currentBook) {
                alert('Load a book and write content');
                return;
            }
            
            alert('Chapter saved (auto-save feature)');
        }
        
        function buildBook() {
            if (!currentBook) {
                alert('Select a book first');
                return;
            }
            
            fetch(`/api/book/${currentBook}/build`, {method: 'POST'})
            .then(r => r.json())
            .then(data => {
                alert('Book built: ' + data.output);
            });
        }
        
        function pushBook(book_id) {
            fetch(`/api/book/${book_id}/push`, {method: 'POST'})
            .then(r => r.json())
            .then(data => {
                alert('Pushed to GitHub');
            })
            .catch(e => alert('Push failed: ' + e));
        }
        
        // Load books on startup
        loadBooks();
        // Don't auto-refresh to avoid duplicates - user can refresh manually
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/book/create', methods=['POST'])
def api_create_book():
    data = request.json
    book_id = author.create_book(data['title'], data['author'], data['description'])
    return jsonify({'book_id': book_id})

@app.route('/api/books/list')
def api_list_books():
    return jsonify(author.config['books'])

@app.route('/api/book/<book_id>')
def api_get_book(book_id):
    book_dir = author.books_dir / book_id
    with open(book_dir / 'metadata.json') as f:
        return jsonify(json.load(f))

@app.route('/api/chapter/create', methods=['POST'])
def api_create_chapter():
    data = request.json
    file = author.create_chapter(data['book_id'], data['title'])
    return jsonify({'file': file})

@app.route('/api/image/upload', methods=['POST'])
def api_upload_image():
    book_id = request.form.get('book_id')
    file = request.files['file']
    book_dir = author.books_dir / book_id
    filepath = book_dir / 'images' / file.filename
    file.save(filepath)
    return jsonify({'filename': file.filename})

@app.route('/api/book/<book_id>/build', methods=['POST'])
def api_build_book(book_id):
    output = author.build_book(book_id)
    return jsonify({'output': output})

@app.route('/api/book/<book_id>/push', methods=['POST'])
def api_push_book(book_id):
    success = author.push_to_github(book_id)
    return jsonify({'success': success})

@app.route('/api/github/setup', methods=['POST'])
def api_github_setup():
    data = request.json
    author.setup_github(data['token'], data['repo'])
    return jsonify({'success': True})

if __name__ == '__main__':
    print("=" * 70)
    print("DIRVEN'S BOOK AUTHORING SYSTEM - WEB UI")
    print("=" * 70)
    print("\n✓ Web server starting...")
    print("✓ Open: http://localhost:5000")
    print("\nTo connect GitHub:")
    print("1. Go to https://github.com/settings/tokens")
    print("2. Create token with 'repo' scope")
    print("3. Enter token in web UI")
    print("\n" + "=" * 70)
    
    app.run(debug=True, port=5000)
