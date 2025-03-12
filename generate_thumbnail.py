from moviepy import VideoFileClip
import os
import sys

VIDEO_DIRECTORY = '/home/ludovic/Vidéos'

def generate_thumbnails(video_directory, thumbnail_directory, force=False):
    if not os.path.exists(thumbnail_directory):
        os.makedirs(thumbnail_directory)

    for root, _, files in os.walk(video_directory, followlinks=True):
        for file in files:
            if file.endswith('.mp4'):
                video_path = os.path.join(root, file)
                thumbnail_path = os.path.join(thumbnail_directory, f"{os.path.splitext(file)[0]}.png")
                
                if os.path.exists(thumbnail_path) and not force:
                    # Si la miniature existe déjà, passer à la vidéo suivante
                    continue

                # Extraire une image à 2 secondes comme miniature
                try:
                    clip = VideoFileClip(video_path)
                    clip.save_frame(thumbnail_path, t=2.0)
                except:
                    print(f"Impossible de générer une miniature pour {video_path}")


if __name__ == '__main__':
    # Take one optional argument: the directory containing the videos
    if len(sys.argv) > 1:
        VIDEO_DIRECTORY = sys.argv[1]
    
    generate_thumbnails(VIDEO_DIRECTORY, 'static/thumbnails', force=True)

