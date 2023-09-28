import tkinter
import customtkinter
import os
from pytube import YouTube
from threading import Timer



# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

def reset():
    font=customtkinter.CTkFont(size=16)
    title.configure(text="Add your Youtbe link", font=font, text_color="white")
    progressBar.set(0)
    progressPourcentage.configure(text="0%")
    # Clear input 
    linkInput.delete(first_index=0, last_index=customtkinter.END)

def on_progress(stream, chunk, bytes_remaining):
    
    # Download size
    total_size = stream.filesize

    # Current Download size
    byte_downloaded = total_size - bytes_remaining

    # Current download percentage
    completionPercentage = byte_downloaded / total_size * 100

    #transform value to string
    percent = str(int(completionPercentage))

    # Display dwonload percentage
    progressPourcentage.configure(text=percent +"%")
    progressPourcentage.update()

    # update progressBar
    progressBar.set(float(completionPercentage) / 100)
    progressBar.update()

def on_video_complete(videoTitle):
    font=customtkinter.CTkFont(size=20)
    title.configure(text= videoTitle + " video completed!", text_color="orange", font=font)
    t = Timer(5.0, reset)
    t.start()

def on_audio_complete(videoTitle):
    font=customtkinter.CTkFont(size=20)
    title.configure(text=videoTitle + " audio completed!", text_color="green", font=font)
    t = Timer(5.0, reset)
    t.start()


def startVideoDowload():
    try:
        ytlink = link.get()
        ytObject = YouTube(ytlink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()
        video.download()
        videoTitle = ytObject.title
        on_video_complete(videoTitle)
            
    except Exception as e:
        # Just print(e) is cleaner and more likely what you want,
        # but if you insist on printing message specifically whenever possible...
        if hasattr(e, 'message'):
            errorLabel.configure(text="Invalid Link, download failed!")
        else:
            errorLabel.configure(text="Invalid Link, download failed!")

def startAudioDowload():
    try:
        ytlink = link.get()
        ytObject = YouTube(ytlink, on_progress_callback=on_progress)
        audio = ytObject.streams.filter(abr='160kbps').last()
        downloadedAudio = audio.download()
        # change extension from mp4 to mp3
        base, ext = os.path.splitext(downloadedAudio)
        mp3Audio = base + '_audio.mp3'
        os.rename(downloadedAudio, mp3Audio)
        videoTitle = ytObject.title
        on_audio_complete(videoTitle)
    except Exception as e:
        # Just print(e) is cleaner and more likely what you want,
        # but if you insist on printing message specifically whenever possible...
        if hasattr(e, 'message'):
            errorLabel.configure(text="Invalid Link, download failed!")
            
        else:
            errorLabel.configure(text="Invalid Link, download failed!")

# App frame
app = customtkinter.CTk()
app.geometry("520x280")
app.title("Youtube Downloader")

# UI element
font=customtkinter.CTkFont(size=16)
title = customtkinter.CTkLabel(app, text="Add your Youtbe link", font=font)
title.pack(padx=10, pady=10)

# Error label
errorLabel = customtkinter.CTkLabel(app, text="", text_color="red", font=font)
errorLabel.pack()

# Creating a var to get the input value
link = tkinter.StringVar()

# Link input
linkInput = customtkinter.CTkEntry(app, width=350, height=40, textvariable=link)
linkInput.pack()

# Video button
videoDownload = customtkinter.CTkButton(app, text="Download Video",fg_color="orange", text_color="black", command=startVideoDowload)
videoDownload.pack(pady=10)

# Audio button
audioDownload = customtkinter.CTkButton(app, text="Download Audio",fg_color="green", command=startAudioDowload)
audioDownload.pack(pady=10)

# Progress percentage
progressPourcentage = customtkinter.CTkLabel(app, text="0%")
progressPourcentage.pack()

# Progress bar
progressBar = customtkinter.CTkProgressBar(app, width=200)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)




# Run app
app.mainloop()

# https://www.youtube.com/watch?v=cyafPNhv6Zc
