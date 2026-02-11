from flask import Flask, request, render_template_string, make_response
import subprocess

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bypass Scanner Pro</title>
    <style>
        body { font-family: sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }
        .card { max-width: 700px; margin: auto; background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; }
        textarea { width: 100%; height: 120px; background: #0d1117; color: #7ee787; border: 1px solid #30363d; border-radius: 6px; padding: 10px; box-sizing: border-box; }
        .btn { display: inline-block; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; border: none; margin-top: 10px; width: 100%; }
        .btn-scan { background: #238636; color: white; }
        .btn-download { background: #21262d; color: #58a6ff; border: 1px solid #30363d; margin-top: 20px; }
        pre { background: #000; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 13px; border: 1px solid #30363d; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Bypass URL Parser (Multi-Link)</h2>
        <form method="POST" action="/scan">
            <label>Paste URLs (one per line):</label>
            <textarea name="urls" placeholder="https://site.com/admin&#10;https://target.com/private" required></textarea>
            <button type="submit" class="btn btn-scan">RUN SCAN</button>
        </form>

        {% if results %}
        <h3>Scan Results:</h3>
        <pre>{{ results }}</pre>
        <form method="POST" action="/download">
            <input type="hidden" name="content" value="{{ results }}">
            <button type="submit" class="btn btn-download">Download as .txt</button>
        </form>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/scan', methods=['POST'])
def scan():
    urls = request.form.get('urls', '').splitlines()
    all_outputs = []
    
    for url in urls:
        url = url.strip()
        if not url: continue
        try:
            # We run the tool for each URL provided
            proc = subprocess.run(['bypass-url-parser', '-u', url], capture_output=True, text=True, timeout=50)
            all_outputs.append(f"--- RESULTS FOR: {url} ---\n{proc.stdout}\n")
        except Exception as e:
            all_outputs.append(f"--- ERROR FOR: {url} ---\n{str(e)}\n")
            
    return render_template_string(HTML_TEMPLATE, results="\n".join(all_outputs))

@app.route('/download', methods=['POST'])
def download():
    content = request.form.get('content', '')
    response = make_response(content)
    response.headers["Content-Disposition"] = "attachment; filename=scan_results.txt"
    response.headers["Content-Type"] = "text/plain"
    return response
