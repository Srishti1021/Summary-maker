import moviepy.editor as mp 


def video_converter(file):
    clip = mp.VideoFileClip(file)

    #to  audio
    clip.audio.write_audiofile("audio.mp3")

