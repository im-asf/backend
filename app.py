from flask import Flask, Response, request
import requests

app = Flask(__name__)

M3U_SOURCE_URL = "https://your-source-url.com/playlist.m3u"  # Replace with your actual M3U source

@app.route('/')
def serve_m3u():
    headers = {"User-Agent": "OTT Navigator"}  # Mimicking OTT Navigator
    try:
        response = requests.get(M3U_SOURCE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return Response(response.text, mimetype='audio/x-mpegurl')
    except requests.RequestException as e:
        return Response(f"#EXTM3U\n#EXTINF:-1,Error: {str(e)}", mimetype='audio/x-mpegurl')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

