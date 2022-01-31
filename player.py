from cProfile import label
from itertools import count
from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import os

global paused
paused = False 
def play_time():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    song = song_box.get(ACTIVE)
    song = f'C:/Music/{song}'
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    current_time +=1
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
        time.sleep(15)
        next_song()
    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        slider_position=int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
    status_bar.after(1000, play_time)

def playsong():
    status_bar.config(text='')
    my_slider.config(value=0)
    global stopped
    stopped = False
    global paused
    paused= False
    song = song_box.get(ACTIVE)
    song = f'C:/Music/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()
    


def pausesong(is_paused):
    global paused
    paused=is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        paused=False
    else:
        pygame.mixer.music.pause()
        paused=True

global stopped
stopped = False

def stopsong():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    global stopped
    stopped = True
    status_bar.config(text='')
    my_slider.config(value=0)

def next_song():
    global count_songs
    status_bar.config(text='')
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one=next_one[0]+1
    song=song_box.get(next_one)
    if (next_one==count_songs):
        song=song_box.get(0)
        next_one=0
    print(song)
    song= f'C:/Music/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

def prev_song():
    next_one = song_box.curselection()
    next_one=next_one[0]-1
    song=song_box.get(next_one)
    if (next_one==-1):
        song=song_box.get(count_songs-1)
        next_one=count_songs-1
    print(song)
    song= f'C:/Music/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)   

def volume(X):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()*100
def slide(x):
    song = song_box.get(ACTIVE)
    song = f'C:/Music/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


root=Tk()
root.title('MUSIC PLAYER')
root.geometry("500x400")
pygame.mixer.init()


song_box= Listbox(root,bg="black",fg="green",width=40)
song_box.pack(pady=10)


back_btn_img= PhotoImage(file='back.png',height=50,width=50)
fwad_btn_img= PhotoImage(file='forward.png',height=50,width=50)
play_btn_img= PhotoImage(file='play.png',height=50,width=50)
paus_btn_img= PhotoImage(file='pause.png',height=50,width=50)
stop_btn_img= PhotoImage(file='stop.png',height=50,width=50)

main_frame=Frame(root)
main_frame.pack(pady=20)

controls_frame= Frame(main_frame)
controls_frame.grid(row=1,column=0,pady=15)


back_btn=Button(controls_frame,image=back_btn_img,borderwidth=0,command=prev_song)
fwad_btn=Button(controls_frame,image=fwad_btn_img,borderwidth=0,command=next_song)
play_btn=Button(controls_frame,image=play_btn_img,borderwidth=0,command=playsong)
paus_btn=Button(controls_frame,image=paus_btn_img,borderwidth=0,command=lambda:pausesong(paused))
stop_btn=Button(controls_frame,image=stop_btn_img,borderwidth=0,command=stopsong)

back_btn.grid(row=0,column=0)
fwad_btn.grid(row=0,column=1)
play_btn.grid(row=0,column=2)
paus_btn.grid(row=0,column=3)
stop_btn.grid(row=0,column=4)

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

my_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2,column=0,pady=10)

volume_slider = ttk.Scale(main_frame,from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=100)
volume_slider.grid(row=1,column=1)

global count_songs
count_songs=0

os.chdir(f'C:/Music/')
songs=os.listdir()
for s in songs:
    count_songs=count_songs+1
    song_box.insert(END,s)
root.mainloop()