import struct
import wave

from pvcheetah import CheetahActivationLimitError, create

access_key='CY2mpNIhK3ELTKzVThK74D9Kntx2jVVnzLZ76XomnfWLqZH9CkLDPA=='
#to transcript the audio file
def transcript(wav_path):
    o = create(
    access_key=access_key,
    enable_automatic_punctuation=True)
    with wave.open(wav_path, 'rb') as f:
        if f.getframerate() != o.sample_rate:
            raise ValueError(
                "invalid sample rate of `%d`. cheetah only accepts `%d`" % (f.getframerate(), o.sample_rate))
        if f.getnchannels() != 1:
            raise ValueError("Can only process single-channel WAV files")
        if f.getsampwidth() != 2:
            raise ValueError("Can only process 16-bit WAV files")

        buffer = f.readframes(f.getnframes())
        audio = struct.unpack('%dh' % (len(buffer) / struct.calcsize('h')), buffer)

    num_frames = len(audio) // o.frame_length
    transcript = ''
    for i in range(num_frames):
        frame = audio[i * o.frame_length:(i + 1) * o.frame_length]
        partial_transcript, _ = o.process(frame)
        print(partial_transcript, end='', flush=True)
        transcript += partial_transcript
    final_transcript = o.flush()
    return final_transcript


if __name__ == "_main_":
    result = transcript(r'recording.wav')
    print(result)

#from pvleopard import *

#def audio_to_text(file):
 #   print("inside audio to text fuction")
  #  o = create(access_key='B6y1g+h9m71kV10cZ3ipSLR/ysNEYB8V9sft+BU07uYb5Lvy5VH38g==')
   # transcript, words = o.process_file(file)
  #  print(transcript)
   # return transcript


#if __name__ == "__main__":
 #   import text_summarizer as ts
  #  out = audio_to_text(r'F:\Python\Internship\Summary Maker\static\uploads\sample-0.mp3')
   # print("output text", out)
    #print("summarize",ts.text_summarizer(out,1))
