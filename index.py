from flask import Flask, request, render_template, send_from_directory
import os
import sys
from pathlib import Path
from generate_thumbnail import generate_thumbnails

app = Flask(__name__)

# Chemin vers le répertoire contenant les vidéos
VIDEO_DIRECTORY = '/home/ludovic/Vidéos'
THUMBNAIL_DIRECTORY = 'static/thumbnails'


@app.route('/')
def index():
    # Calculate the number of videos in the directory and subdirectories
    video_count = 0
    for root, _, files in os.walk(VIDEO_DIRECTORY, followlinks=True):
        for file in files:
            if file.endswith('.mp4'):
                video_count += 1

    return render_template('index.html', video_count=video_count)


@app.route('/search', methods=['GET'])
def search():    
    keyword = request.args.get('keyword', '')
    videos = find_videos(keyword)
    return render_template('results.html', keyword=keyword, videos=videos)


@app.route('/watch/<path:filename>')
def watch(filename):
    generate_thumbnails(VIDEO_DIRECTORY, THUMBNAIL_DIRECTORY)
    return send_from_directory(VIDEO_DIRECTORY, filename)


@app.route('/thumbnails/<path:filename>')
def thumbnails(filename):
    return send_from_directory(THUMBNAIL_DIRECTORY, filename)


def find_videos(keyword):
    videos = []
    for root, _, files in os.walk(VIDEO_DIRECTORY, followlinks=True):
        for file in files:
            if keyword.lower() in file.lower() and file.endswith('.mp4'):
                file_path = Path(file)
                relative_path = os.path.relpath(os.path.join(root, file), VIDEO_DIRECTORY)

                thumbnail_path = f"{file_path.stem}.png"
                videos.append((relative_path, thumbnail_path))
    return videos


if __name__ == '__main__':
    # Take one optional argument: the directory containing the videos
    if len(sys.argv) > 1:
        VIDEO_DIRECTORY = sys.argv[1]

    app.run(debug=True)

