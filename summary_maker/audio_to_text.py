from pvleopard import *
import os
from text_summarizer import text_summarizer as ts

def audio_to_text(file):
    if os.path.exists(file):
        access_key =  "/uxvfvfUslKpwkNjG5lBIspKK0DFCS0uGp/V16HWTTtJA8a0osOZxA=="
        o = create( access_key=access_key )
        print("file exists")
        leopard = create( access_key=access_key )
        transcript, words = leopard.process_file(file)
        return transcript
    
def summarize_audio(file):
    transcript = audio_to_text(file)
    print(transcript)
    summary = ts(transcript, 3)
    print(summary)
    return summary

if __name__ == "_main_":
    sa = summarize_audio(r"static(img\Recording (2).m4a",)
    print(sa)