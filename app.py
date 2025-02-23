from flask import Flask, request, render_template, jsonify import yt_dlp

app = Flask(name)

def download_video(url): options = { 'format': 'best', 'outtmpl': 'downloads/%(title)s.%(ext)s', }

with yt_dlp.YoutubeDL(options) as ydl:
    info = ydl.extract_info(url, download=False)
    return info.get('url', None), info.get('title', 'Unknown')

@app.route('/') def home(): return render_template('index.html')

@app.route('/download', methods=['POST']) def download(): url = request.form.get('url') if not url: return jsonify({'error': 'No URL provided'}), 400

video_url, title = download_video(url)
if video_url:
    return jsonify({'video_url': video_url, 'title': title})
else:
    return jsonify({'error': 'Failed to fetch video'}), 500

if name == 'main': from os import environ port = int(environ.get('PORT', 5000)) app.run(host='0.0.0.0', port=port)

