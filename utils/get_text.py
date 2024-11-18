# this code is contributed by Pulkit Dhingra
from pytubefix import YouTube
from pytubefix.cli import on_progress

# get audio from video
import moviepy.editor as mp
import os
from pydub import AudioSegment 

# speech recognition
import speech_recognition as sr

# download the video
def download(url,filename,directory = "video" ,save_format = "mp4"):

    youtube_url = url
    yt = YouTube(youtube_url, on_progress_callback = on_progress)
    print(yt.title)
    ys = yt.streams.get_highest_resolution()
    save_path = directory + "/" +filename + "." + save_format
    if os.path.exists(directory):
        ys.download(filename = save_path,max_retries = 3)
    else:
        os.mkdir(directory)
        ys.download(filename =save_path,max_retries = 3)


# get audio file from the video 
## this will be used for speech to text transfer 
def audio_from_video(video_file,audio_filename,directory = 'audio',save_format = "wav"):
    
    save_path = directory + '/' + audio_filename + '.' + save_format
    clip = mp.VideoFileClip(video_file)
    if os.path.exists(directory):
        clip.audio.write_audiofile(save_path)
    else:
        os.mkdir(directory)
        clip.audio.write_audiofile(save_path)

# speech to text
def get_text_from_audio(target_file,save_filename,directory = 'text_output'):
    
    # Initialize the recognizer
    r = sr.Recognizer()
    song = AudioSegment.from_mp3(target_file) 

    # pydub does things in milliseconds 
    ten_seconds = 2 * 60 * 1000

    # get the number of segments
    # Calculate the number of segments
    num_segments = math.ceil(len(audio) / segment_duration)

    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, len(audio))
        
        segment = audio[start_time:end_time]
        segment.export(f"output_segment_{i+1}.mp3", format="mp3")
        print(f"Exported: output_segment_{i+1}.mp3")


    with sr.AudioFile(target_file) as source:
        audio = r.record(source)

        # Adjust the recognizer sensitivity to ambient noise
        r.adjust_for_ambient_noise(source, duration=0.3)

    s = r.recognize_google(audio)

    if os.path.exists(directory):
        filename = directory + '/' + save_filename + '.txt'
        text_file = open(filename, "w")
        text_file.write("%s" % s)
        text_file.close()
    else:
        os.mkdir(directory)
        filename = directory + '/' + save_filename + '.txt'
        text_file = open(filename, "w")
        text_file.write("%s" % s)
        text_file.close()