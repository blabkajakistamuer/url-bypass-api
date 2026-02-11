from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/scan', methods=['GET'])
def scan():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "No URL provided. Use ?url=http://..."}), 400

    try:
        # We call the 'bypass-url-parser' command directly.
        # Vercel's environment has curl installed by default.
        process = subprocess.run(
            ['bypass-url-parser', '-u', target_url],
            capture_output=True,
            text=True,
            check=True
        )
        return f"<pre>{process.stdout}</pre>"
    except subprocess.CalledProcessError as e:
        return f"<h3>Error during scan:</h3><pre>{e.output}\n{e.stderr}</pre>", 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for the home page
@app.route('/')
def home():
    return "<h1>URL Bypass API</h1><p>Append <b>/scan?url=[TARGET]</b> to the URL.</p>"

