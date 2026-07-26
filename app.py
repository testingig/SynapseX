import os
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory database list to keep everything in one script
games_db = []

# Single HTML template containing both the Frontend UI and Backend logic
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Single-Script Unrestricted Hub</title>
    <style>
        :root {
            --bg-color: #0f1015;
            --card-bg: #1a1b24;
            --accent: #ff3366;
            --text-main: #ffffff;
            --text-muted: #8a8d9b;
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 0;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
            border-bottom: 1px solid #2a2b38;
        }
        .logo { font-weight: 800; font-size: 1.5rem; color: var(--accent); }
        .container { max-width: 1000px; margin: 40px auto; padding: 0 20px; }
        .upload-box {
            background-color: var(--card-bg);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #2a2b38;
            margin-bottom: 40px;
        }
        input, button {
            padding: 10px 15px;
            margin-right: 10px;
            border-radius: 6px;
            border: 1px solid #2a2b38;
            background: #252633;
            color: white;
        }
        button.upload-btn {
            background-color: var(--accent);
            border: none;
            font-weight: 600;
            cursor: pointer;
        }
        button.upload-btn:hover { opacity: 0.9; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 20px;
        }
        .card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #2a2b38;
        }
        .card-title { font-weight: 600; font-size: 1.1rem; margin-bottom: 8px; }
        .card a { color: var(--accent); text-decoration: none; font-size: 0.9rem; }
    </style>
</head>
<body>

    <header>
        <div class="logo">SOLOHUB</div>
    </header>

    <div class="container">
        <h1>Unrestricted File & Game Portal</h1>
        <p style="color: var(--text-muted);">Upload any project, script, or build file with zero platform filters.</p>
        
        <div class="upload-box">
            <form action="/upload" method="POST" enctype="multipart/form-data">
                <input type="text" name="title" placeholder="Project Name" required>
                <input type="file" name="gamefile" required>
                <button type="submit" class="upload-btn">Upload File</button>
            </form>
        </div>

        <h2>Uploaded Builds</h2>
        <div class="grid">
            {% for game in games %}
                <div class="card">
                    <div class="card-title">{{ game.title }}</div>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">File: {{ game.filename }}</p>
                    <a href="/download/{{ game.filename }}">Download Build</a>
                </div>
            {% else %}
                <p style="color: var(--text-muted);">No projects uploaded yet.</p>
            {% endfor %}
        </div>
    </div>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, games=games_db)

@app.route('/upload', methods=['POST'])
def upload_file():
    title = request.form.get('title')
    file = request.files.get('gamefile')
    
    if file and title:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        games_db.append({'title': title, 'filename': filename})
        
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
