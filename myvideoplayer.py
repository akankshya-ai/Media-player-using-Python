import time
from tkinter import *
from tkinter import filedialog
import pygame
import os
from PIL import Image, ImageTk
import threading
from moviepy.editor import VideoFileClip

root = Tk()
root.title("Beat Blazers")
root.geometry("600x900+300+20")
root.configure(background="#333333")
pygame.mixer.init()

video_thread = None
stop_video_event = threading.Event()

current_mode = None  # "music" or "video"

def AddMusic():
    global current_mode
    current_mode = "music"
    path = filedialog.askdirectory()
    if path:
        Playlist.delete(0, END)
        os.chdir(path)
        songs = os.listdir(path)
        for song in songs:
            if song.endswith(".mp3") or song.endswith(".wav") or song.endswith(".ogg"):
                Playlist.insert(END, song)
        if Playlist.size() > 0:
            PlayMusic()

def PlayMusic():
    global current_mode
    if current_mode != "music":
        return
    Music_Name = Playlist.get(ACTIVE)
    if Music_Name.endswith(".mp3") or Music_Name.endswith(".wav") or Music_Name.endswith(".ogg"):
        print(Music_Name)
        try:
            pygame.mixer.music.load(Music_Name)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error loading {Music_Name}: {e}")
    else:
        print("Selected file is not a valid audio format")

def AddVideo():
    global current_mode
    current_mode = "video"
    path = filedialog.askdirectory()
    if path:
        Playlist.delete(0, END)
        os.chdir(path)
        videos = os.listdir(path)
        for video in videos:
            if video.endswith(".mp4") or video.endswith(".avi") or video.endswith(".mov"):
                Playlist.insert(END, video)

def PlayVideo():
    global current_mode, video_thread, stop_video_event
    if current_mode != "video":
        return
    video_path = Playlist.get(ACTIVE)
    if video_path.endswith(".mp4") or video_path.endswith(".avi") or video_path.endswith(".mov"):
        print(f"Playing video: {video_path}")
        stop_video_event.clear()
        video_thread = threading.Thread(target=play_video_with_sound, args=(video_path,))
        video_thread.start()
    else:
        print("Selected file is not a valid video format")

def StopVideo():
    global stop_video_event
    stop_video_event.set()
    pygame.mixer.music.stop()

def play_video_with_sound(video_path):
    try:
        clip = VideoFileClip(video_path)
        audio_thread = threading.Thread(target=play_audio, args=(clip,))
        audio_thread.start()
        for frame in clip.iter_frames(fps=24, dtype='uint8'):
            if stop_video_event.is_set():
                break
            frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
            label_video.config(image=frame_image)
            label_video.image = frame_image
            label_video.update_idletasks()  # Ensure the label is updated
            time.sleep(1 / 24)  # Adjust the delay to match the video frame rate
        clip.close()
    except Exception as e:
        print(f"Error playing video {video_path}: {e}")

def play_audio(clip):
    try:
        clip.audio.preview()
    except Exception as e:
        print(f"Error playing audio: {e}")

# Adjust the lower frame position
lower_frame = Frame(root, bg="#333333", width=600, height=150)
lower_frame.place(x=20, y=500)

# Frame for music playlist, placed at the top
Frame_Music = Frame(root, bd=2, relief=RIDGE)
Frame_Music.place(x=0, y=0, width=600, height=150)

Scroll = Scrollbar(Frame_Music)
Playlist = Listbox(Frame_Music, width=100, font=("Times new roman", 10), bg="#333333", fg="white", selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=Scroll.set)
Scroll.config(command=Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=RIGHT, fill=BOTH)

ButtonPlay = PhotoImage(file="play.png")
Button(root, image=ButtonPlay, bg="#00FF00", bd=0, height=60, width=60, command=PlayMusic).place(x=265, y=150)

ButtonStop = PhotoImage(file="music.png")
Button(root, image=ButtonStop, bg="#00FF00", bd=0, height=60, width=60, command=StopVideo).place(x=150, y=150)

#ButtonPause = PhotoImage(file="play-icon.png")
#Button(root, image=ButtonPause, bg="#FFFFFF", bd=0, height=60, width=60, command=pygame.mixer.music.pause).place(x=350, y=150)

ButtonVideo = PhotoImage(file="clapperboard.png")
Button(root, image=ButtonVideo, bg="#00FF00", bd=0, height=60, width=60, command=PlayVideo).place(x=370, y=150)

Button(root, text="Browse Music", width=59, height=1, font=("calibri", 12, "bold"), fg="Black", bg="#00FF00", command=AddMusic).place(x=60, y=250)

Button(root, text="Browse Video", width=59, height=1, font=("calibri", 12, "bold"), fg="Black", bg="#00FF00", command=AddVideo).place(x=60, y=300)

# Label for video display
label_video = Label(root)
label_video.place(x=0, y=350, width=600, height=250)

root.mainloop()
