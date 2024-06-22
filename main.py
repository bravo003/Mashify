import os
import re
import time
import zipfile
import urllib.error
from mail import send_mail
os.environ["IMAGEIO_FFMPEG_EXE"] = "ffmpeg"
from youtube_search import YoutubeSearch
from pytube import YouTube, exceptions
from moviepy.editor import VideoFileClip, concatenate_audioclips

def download_videos(artist, number_of_videos):
    downloaded_count = 0
    search_query = f"{artist} music video"
    search_results = YoutubeSearch(search_query, max_results=number_of_videos + 20).to_dict()
    
    for result in search_results:
        try:
            yt_video = YouTube(f'https://youtube.com{result["url_suffix"]}')
            video_stream = yt_video.streams.filter(file_extension='mp4').first()
            destination_folder = 'VideoFiles'
            downloaded_video_path = video_stream.download(output_path=destination_folder)
        except (exceptions.VideoUnavailable, urllib.error.HTTPError):
            continue
        else:
            downloaded_count += 1
            if downloaded_count == number_of_videos:
                break

def extract_audio_from_videos(output_format="mp3"):
    video_folder = "VideoFiles"
    audio_clips = []
    
    for file in os.listdir(video_folder):
        if file.endswith(".mp4"):
            video_path = os.path.join(video_folder, file)
            video_clip = VideoFileClip(video_path)
            audio_clip = video_clip.audio
            audio_clips.append(audio_clip)
    
    return audio_clips

def trim_audio_clips(audio_clips, duration):
    trimmed_clips = []
    
    for clip in audio_clips:
        trimmed_clip = clip.subclip(10, 10 + duration)
        trimmed_clips.append(trimmed_clip)
    
    return trimmed_clips

def create_mashup(audio_clips, output_filename='mashup'):
    combined_audio = concatenate_audioclips(audio_clips)
    combined_audio.write_audiofile(f"{output_filename}.mp3")

def create_zip_file(file_path):
    zip_filename = 'mashup.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        zip_file.write(file_path, compress_type=zipfile.ZIP_DEFLATED)
    return zip_filename

def main_script(artist, video_count, clip_duration, email, output_filename='mashup'):
    download_videos(artist, video_count)
    audio_clips = extract_audio_from_videos()
    trimmed_clips = trim_audio_clips(audio_clips, clip_duration)
    create_mashup(trimmed_clips, output_filename)
    zip_file_path = create_zip_file(f"{output_filename}.mp3")
    send_mail(email, zip_file_path)