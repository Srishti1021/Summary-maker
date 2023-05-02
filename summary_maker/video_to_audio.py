import moviepy.editor as mp 
from audio_to_text import summarize_audio

def video_converter(file):
    clip = mp.VideoFileClip(file)

    #to  audio
    clip.audio.write_audiofile("audio.mp3")

