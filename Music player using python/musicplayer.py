# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 21:30:06 2021

@author: Soumyojyoti Dutta
"""
from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
root = Tk()
root.title('Ragini Music player')

root.geometry("500x400")
#initialize Pygame Mixer
pygame.mixer.init()

#add song function
def add_song():
    song = filedialog.askopenfilename(initialdir='song/', title="Choose a song", filetypes= (("mp3 Files ", "*.MP3"), ))
    songlist.insert(END, song)
def addmanysong():
    songs = filedialog.askopenfilenames(initialdir='song/', title="Choose multiple song", filetypes= (("mp3 Files ", "*.MP3"), ))
    for song in songs:
        songlist.insert(END, song)
def remove_song():
    songlist.delete(ANCHOR)
    pygame.mixer.music.stop()
def removeallsong():
    songlist.delete(0,END)
    pygame.mixer.music.stop()

#play selected song
def play():
    global stopped
    stopped = False
    song = songlist.get(ACTIVE)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #call the playtime
    play_time()
    #update slider to position
    #slider_pos = int(song_length)
    #my_slider.config(to=slider_pos,value=1)
    # Get current Volume
    current_volume = pygame.mixer.music.get_volume()
    # Times by 100 to make it easier to work with
    current_volume = current_volume * 100
    #slider_label.config(text=current_volume * 100)

    # Change Volume Meter Picture
    if int(current_volume) < 1:
        volume_meter.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <= 25:
        volume_meter.config(image=vol1)
    elif int(current_volume) >= 25 and int(current_volume) <= 50:
        volume_meter.config(image=vol2)
    elif int(current_volume) >= 50 and int(current_volume) <= 75:
        volume_meter.config(image=vol3)
    elif int(current_volume) >= 75 and int(current_volume) <= 100:
        volume_meter.config(image=vol4)
#stop running song

def stop():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)
    # Stop Song From Playing
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    # Clear The Status Bar
    status_bar.config(text='')

    # Set Stop Variable To True
    global stopped
    stopped = True 

    # Get current Volume
    current_volume = pygame.mixer.music.get_volume()
    # Times by 100 to make it easier to work with
    current_volume = current_volume * 100
    #slider_label.config(text=current_volume * 100)

    # Change Volume Meter Picture
    if int(current_volume) < 1:
        volume_meter.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <= 25:
        volume_meter.config(image=vol1)
    elif int(current_volume) >= 25 and int(current_volume) <= 50:
        volume_meter.config(image=vol2)
    elif int(current_volume) >= 50 and int(current_volume) <= 75:
        volume_meter.config(image=vol3)
    elif int(current_volume) >= 75 and int(current_volume) <= 100:
        volume_meter.config(image=vol4)


#pause current song
global paused
paused = False
def pause(ispaused):
    global paused
    paused = ispaused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True
#play foreward song
def next_song():
    nextsong = songlist.curselection()
    nextsong = nextsong[0]+1
    song = songlist.get(nextsong)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    songlist.selection_clear(0, END)
    songlist.activate(nextsong)
    songlist.selection_set(nextsong,last=None)
#play previous song
def previous_song():
    backsong = songlist.curselection()
    backsong = backsong[0]-1
    song = songlist.get(backsong)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    pygame.mixer.music.play(loops=0)
    songlist.selection_clear(0, END)
    songlist.activate(backsong)
    songlist.activate(backsong)
    songlist.selection_set(backsong,last=None)
#length,time info
def play_time():
    # Check for double timing
    if stopped:
        return 
    # Grab Current Song Elapsed Time
    current_time = pygame.mixer.music.get_pos() / 1000

    # throw up temp label to get data
    #slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')
    # convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # Get Currently Playing Song
    #current_song = song_box.curselection()
    #Grab song title from playlist
    song = songlist.get(ACTIVE)
    # add directory structure and mp3 to song title
    
    # Load Song with Mutagen
    song_mut = MP3(song)
    # Get song Length
    global song_length
    song_length = song_mut.info.length
    # Convert to Time Format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # Increase current time by 1 second
    current_time +=1
    
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        # Update Slider To position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        # Update Slider To position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        
        # convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        # Output time to status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

        # Move this thing along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
    # Output time to status bar
    status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

    # Update slider position value to current song position...
    #my_slider.config(value=int(current_time))
    
    
    # update time
    status_bar.after(1000, play_time)
#create slider
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = songlist.get(ACTIVE)
    

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
def volume(x):
        pygame.mixer.music.set_volume(volume_slider.get())
        # Get current Volume
        current_volume = pygame.mixer.music.get_volume()
        # Times by 100 to make it easier to work with
        current_volume = current_volume * 100
        #slider_label.config(text=current_volume * 100)
         # Change Volume Meter Picture
        if int(current_volume) < 1:
            volume_meter.config(image=vol0)
        elif int(current_volume) > 0 and int(current_volume) <= 25:
            volume_meter.config(image=vol1)
        elif int(current_volume) >= 25 and int(current_volume) <= 50:
            volume_meter.config(image=vol2)
        elif int(current_volume) >= 50 and int(current_volume) <= 75:
            volume_meter.config(image=vol3)
        elif int(current_volume) >= 75 and int(current_volume) <= 100:
            volume_meter.config(image=vol4) 

   
    
    


# Create Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)
#create Playlist box
songlist = Listbox(master_frame, bg="black", fg="green", width=60, selectbackground="yellow", selectforeground="grey")
songlist.grid(row=0, column=0)
#link control icons
back_btn_img = PhotoImage(file='img/back50.png')
forward_btn_img =  PhotoImage(file='img/forward50.png')
play_btn_img =  PhotoImage(file='img/play50.png')
pause_btn_img =  PhotoImage(file='img/pause50.png')
stop_btn_img =  PhotoImage(file='img/stop50.png')
#create control
controls_frame = Frame(root)
controls_frame.pack()
#button
global vol0
global vol1
global vol2
global vol3
global vol4
vol0 = PhotoImage(file='img/volume0.png')
vol1 = PhotoImage(file='img/volume1.png')
vol2 = PhotoImage(file='img/volume2.png')
vol3 = PhotoImage(file='img/volume3.png')
vol4 = PhotoImage(file='img/volume4.png')

# Create Player Control Frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

# Create Volume Meter
volume_meter = Label(master_frame, image=vol0)
volume_meter.grid(row=1, column=1, padx=10)

# Create Volume Label Frame
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=30)
backbtn = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forwardbtn = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
playbtn = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pausebtn = Button(controls_frame, image=pause_btn_img, borderwidth=0, command= lambda: pause(paused))
stopbtn = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

backbtn.grid(row=0, column=1, padx=10) 
forwardbtn.grid(row=0, column=4, padx=10)
playbtn.grid(row=0, column=2, padx=10)
pausebtn.grid(row=0, column=3, padx=10)
stopbtn.grid(row=0, column=0, padx=10)

#create Menu
my_menu = Menu(root)
root.config(menu=my_menu)
#add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist", command=add_song)
add_song_menu.add_command(label="Add multiple song to playlist", command=addmanysong)
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Delete Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove one song from the playlist", command=remove_song)
remove_song_menu.add_command(label="Remove all song from the playlist", command=removeallsong)

#create status bar
status_bar = Label(root, text = '', bd=1, relief=GROOVE, anchor = E)
status_bar.pack(fill=X, side=BOTTOM,ipady=2)
# Create Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)
# Create Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)
root.mainloop()