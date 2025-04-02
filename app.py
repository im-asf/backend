from flask import Flask, Response, request, render_template_string
import requests

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Enter M3U URL</title>
</head>
<body>
    <h2>Enter M3U URL</h2>
    <form method="get" action="/proxy">
        <input type="text" name="url" placeholder="Enter M3U URL" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''

cached_m3u = ""  # Store fetched M3U data

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/proxy')
def proxy():
    global cached_m3u
    m3u_url = request.args.get('url')
    if not m3u_url:
        return "Missing M3U URL", 400
    
    headers = {"User-Agent": "OTT Navigator"}  # Mimicking OTT Navigator
    try:
        response = requests.get(m3u_url, headers=headers, timeout=10)
        response.raise_for_status()
        cached_m3u = response.text  # Store the M3U contents
        return f"Your M3U is ready: <a href='/playlist.m3u'>Click here</a>", 200
    except requests.RequestException as e:
        return f"Error fetching M3U: {str(e)}", 500

@app.route('/playlist.m3u')
def serve_cached_m3u():
    global cached_m3u
    if not cached_m3u:
        return "No M3U file cached yet!", 404
    return Response(cached_m3u, mimetype='audio/x-mpegurl')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
