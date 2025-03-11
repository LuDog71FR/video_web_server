from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)

# Chemin vers le répertoire contenant les vidéos
VIDEO_DIRECTORY = '~/Vidéos'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    videos = find_videos(keyword)
    return render_template('results.html', keyword=keyword, videos=videos)


@app.route('/watch/<path:filename>')
def watch(filename):
    return send_from_directory(VIDEO_DIRECTORY, filename)


def find_videos(keyword):
    videos = []
    for root, _, files in os.walk(VIDEO_DIRECTORY):
        for file in files:
            if keyword.lower() in file.lower() and file.endswith('.mp4'):
                videos.append(os.path.relpath(os.path.join(root, file), VIDEO_DIRECTORY))
    return videos


if __name__ == '__main__':
    app.run(debug=True)

