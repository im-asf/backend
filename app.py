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
    <form method="get" action="/">
        <input type="text" name="url" placeholder="Enter M3U URL" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''

def convert_mpd_to_hls(mpd_url):
    # Placeholder function: Replace with actual MPD-to-HLS conversion
    return mpd_url.replace("manifest.mpd", "playlist.m3u8")

@app.route('/')
def serve_m3u():
    m3u_url = request.args.get('url')
    if not m3u_url:
        return render_template_string(HTML_FORM)
    
    headers = {"User-Agent": "OTT Navigator"}  # Mimicking OTT Navigator
    try:
        response = requests.get(m3u_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Convert MPD URLs to HLS URLs in the playlist
        m3u_content = response.text.replace("manifest.mpd", "playlist.m3u8")
        return Response(m3u_content, mimetype='audio/x-mpegurl')
    except requests.RequestException as e:
        return Response(f"#EXTM3U\n#EXTINF:-1,Error: {str(e)}", mimetype='audio/x-mpegurl')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
