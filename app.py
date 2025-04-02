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
    <form method="get" action="/playlist.m3u">
        <input type="text" name="url" placeholder="Enter M3U URL" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/playlist.m3u')
def serve_m3u():
    m3u_url = request.args.get('url')
    if not m3u_url:
        return Response("#EXTM3U\n#EXTINF:-1,Error: No URL provided", mimetype='audio/x-mpegurl')
    
    headers = {"User-Agent": "OTT Navigator"}  # Mimicking OTT Navigator
    try:
        response = requests.get(m3u_url, headers=headers, timeout=10, stream=True)
        response.raise_for_status()
        
        def generate():
            for chunk in response.iter_content(chunk_size=1024):
                yield chunk
        
        return Response(generate(), content_type='audio/x-mpegurl')
    except requests.RequestException as e:
        return Response(f"#EXTM3U\n#EXTINF:-1,Error: {str(e)}", mimetype='audio/x-mpegurl')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
