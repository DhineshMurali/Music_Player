import os
import smtplib
import sqlite3
from tkinter import *
import pygame
import requests
import re
import tkinter as tk
from tkinter import ttk

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
root = Tk()
root.geometry('500x400')
root.title("B&M-Books and Music")
root.configure(background="black")

bg = PhotoImage(file="bmpic1.png")

canvas1 = Canvas(root, width=400,
                 height=400)

canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg,
                     anchor="nw")
canvas1.create_text(200, 350, text="WELCOME TO B&M APP",
                    font=("times new roman", 15, " bold"))

textin = StringVar()
textinn = StringVar()
text = StringVar()

db = sqlite3.connect('D:/python project/bandm.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS people(name TEXT, phone TEXT)")
db.commit()

lab = Label(root, text='User-Name:', font= ('none 13 bold'))
lab.place(x=20, y=10)

entname = Entry(root, width=20, font=('none 13 bold'), textvar=textin)
entname.place(x=160, y=10)

entphone = Entry(root, width=20, font=(
    'none 13 bold'), textvar=textinn, show="*")
entphone.place(x=160, y=50)

entmail = Entry(root, width=20, font=('none 13 bold'), textvar=text)
entmail.place(x=160,y=90)

lab1 = Label(root, text='Password:', font=('none 13 bold'))
lab1.place(x=20, y=50)

mail_lbl = Label(root, text='E-Mail:',font=('none 13 bold'))
mail_lbl.place(x=20,y=90)

lbl_text = Label(root)
lbl_text.place(x=160, y=110)

def insert():

    name1 = textin.get()
    phone1 = textinn.get()
    mail1 = text.get()
    if (re.search(regex, mail1)):
        conn = sqlite3.connect('D:/python project/bandm.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO people(name, phone, mail) VALUES(?,?,?)', (name1, phone1, mail1))
            lbl_text.config(text="sign-in sucessfull!", fg="green")
            db.close()
    else:
        lbl_text.config(text="enter a valid mail address",fg="red")
def select_page():

    Top = Toplevel()
    Top.title("BOOK OR MUSIC?")
    Top.geometry("400x300")
    Top.configure(background="light blue")

    book_lbl = Label(Top, text='DOWNLOAD THE BOOKS HERE',
                     font=("times new roman", 15, 'bold'), fg="light blue", bg="blue")
    book_lbl.place(x=35, y=50)
    book = Button(Top, padx=2, pady=2, text='BOOKS',
                  command=bookdownloader, font=('none 13 bold'), fg="light blue", bg="dark blue")
    book.place(x=130, y=90)
    music_lbl = Label(Top, text='DOWNLOAD/PLAY MUSIC HERE',
                      font=("times new roman", 15, 'bold'), fg="light blue", bg="blue")
    music_lbl.place(x=35, y=160)
    music = Button(Top, padx=2, pady=2, text='MUSIC',command=musicplayer,
                   font=('none 13 bold'), fg="light blue", bg="dark blue")
    music.place(x=130, y=200)
    back = Button(Top, text="Back", command=Top.destroy,
                  font=("times new roman", 12, "bold"))
    back.place(x=320, y=0)


def show():
    connt = sqlite3.connect('D:/python project/bandm.db')
    cursor = connt.cursor()

    if entname.get() == "" or entphone.get() == "" or entmail.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `people` WHERE `name` = ? AND `phone` = ? AND `mail` = ?",
                       (entname.get(), entphone.get(), entmail.get()))
        if cursor.fetchone() is not None:
            select_page()

            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password or mail-id", fg="red")

    cursor.close()
    db.close()


name = StringVar()
phone = StringVar()
mail = StringVar()


def musicplayer():
    mus = Toplevel()
    mus.title("Music Player")
    mus.geometry("600x400")
    pygame.init()
    pygame.mixer.init()
    track = StringVar()
    status = StringVar()

    def playsong():
        track.set(playlist.get(ACTIVE))
        status.set("-Playing")
        pygame.mixer.music.load(playlist.get(ACTIVE))
        pygame.mixer.music.play()

    def stopsong():

        status.set("-Stopped")
        pygame.mixer.music.stop()

    def pausesong():

        status.set("-Paused")
        pygame.mixer.music.pause()

    def unpausesong():

        status.set("-Playing")

        pygame.mixer.music.unpause()

    ttk.Label(mus, text="Select the Song Type :",
              font=("Times New Roman", 10)).place(x=20,y=200)

    songchoosen = ttk.Combobox(mus, width=27)

    # Adding combobox drop down list
    songchoosen['values'] = ["FOLK",
                              " HIP_HOP",
                              " MELODY"]
    songchoosen.current(1)
    songchoosen.place(x=250, y=200)

    trackframe = LabelFrame(mus, text="CUREENT SONG", font=("times new roman", 15, "bold"), bg="Black",
                                fg="gold", bd=5, relief=RAISED)
    trackframe.place(x=0, y=0, width=600, height=100)
    songtrack = Label(trackframe, textvariable=track, width=20, font=("times new roman", 24, "bold"), bg="Orange",fg="gold").grid(row=0, column=0, padx=10, pady=5)
    trackstatus = Label(trackframe, textvariable=status, font=("times new roman", 24, "bold"), bg="orange", fg="gold").grid(row=0,column=1,padx=10,pady=5)

    buttonframe = LabelFrame(mus, text="Controls", font=("times new roman", 15, "bold"), bg="black",
                             fg="gold", bd=5)
    buttonframe.place(x=0, y=100, width=600, height=100)
    playbtn = Button(buttonframe, text="PLAYSONG", command=playsong, width=10, height=1,
                     font=("times new roman", 14, "bold"), fg="navyblue", bg="pink").grid(row=0, column=0, padx=10,
                                                                                          pady=5)
    pausebtn = Button(buttonframe, text="PAUSE", command=pausesong, width=8, height=1,
                     font=("times new roman", 14, "bold"), fg="navyblue", bg="pink").grid(row=0, column=1, padx=10,
                                                                                          pady=5)
    unpausebtn = Button(buttonframe, text="UNPAUSE", command=unpausesong, width=8, height=1,
                     font=("times new roman", 14, "bold"), fg="navyblue", bg="pink").grid(row=0, column=2, padx=10,
                                                                                          pady=5)
    stopbtn = Button(buttonframe, text="STOPSONG", command=stopsong, width=10, height=1,
                     font=("times new roman", 14, "bold"), fg="navyblue", bg="pink").grid(row=0, column=3, padx=10,pady=5)

    bach_mbtn = Button(buttonframe, text= "BACK",command = mus.destroy,width = 5,height=1,font=("times new roman", 14, "bold"), fg="navyblue", bg="pink").grid(row=0, column=4, padx=10,pady=5)

    songsframe = LabelFrame(mus, text="Song Playlist", font=("times new roman", 15, "bold"), bg="black",
                            fg="gold", bd=5, relief=RAISED)
    songsframe.place(x=0, y=220, width=600, height=200)

    scrol_y = Scrollbar(songsframe, orient=VERTICAL)

    playlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectbackground="gold", selectmode=SINGLE,
                       font=("times new roman", 12, "bold"), bg="silver", fg="navyblue", bd=5, relief=GROOVE)

    scrol_y.pack(side=RIGHT, fill=Y)
    scrol_y.config(command=playlist.yview)
    playlist.pack(fill=BOTH)

    os.chdir("D:\songs")

    songtracks = os.listdir()

    for i in songtracks:
        playlist.insert(END, i)


def bookdownloader():
    top = Toplevel()
    top.title("Download books here")
    top.geometry("550x250")
    top.configure(background="black")
    top.url = StringVar()
    top.status = StringVar()
    top.status.set("--/--")

    def download():
        if top.url.get() == "":
            top.status.set("URL NOT SPECIFIED")
        else:
            try:

                top.status.set("Downloading...")
                top.update()

                Requests = requests.get(top.url.get())

                if Requests.status_code == requests.codes.ok:

                    file = open("download", "wb")
                    file.write(Requests.content)
                    file.close()

                    top.status.set("Download Completed")
                else:
                    top.status.set(Requests.status_code)
            except:
                top.status.set("Error in Downloading")

    def show_books():
        bd = Toplevel()
        bd.geometry("300x300")
        connt = sqlite3.connect('D:/python project/bandm.db')
        cursor = connt.cursor()
        cursor.execute('SELECT * FROM bookDetails')

        i = 0
        for book in cursor.fetchall():
            for j in range(len(book)):
                e = Entry(bd, width=10, fg='blue')
                e.grid(row=i, column=j)
                e.insert(END, book[j])

            i = i + 1



    back = Button(top, text="Back", command=top.destroy,
                  font=("times new roman", 12, "bold"))
    back.place(x=450)
    url_lbl = Label(top, text="Book URL:", compound=LEFT, font=(
        "times new roman", 15, "bold"), bg="grey", fg="gold")
    url_lbl.place(x=50, y=50)
    url_txt = Entry(top, bd=2, width=25, textvariable=top.url,
                    relief=SUNKEN, font=("times new roman", 15))
    url_txt.place(x=180, y=50)
    dwn_btn = Button(top, text="Download", command=download, width=10, font=(
        "times new roman", 14, "bold"), bg="gold", fg="grey")
    dwn_btn.place(x=350, y=100)
    book_btn = Button(top, text="Show Book URL", command=show_books, width=13, font=(
        "times new roman", 14, "bold"), bg="gold", fg="grey")
    book_btn.place(x=180, y=100)
    status_lbl = Label(top, textvariable=top.status, font=(
        "times new roman", 14, "bold"), bg="grey", fg="white")
    status_lbl.place(x=200, y=150)


def send_message():
    address_info = text.get()

    print(address_info)

    sender_email = "ottplatform.gui@gmail.com"

    sender_password = "CS1001&19"

    email_body_info = "Thank you for creating a account in B&M application"

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()

    server.login(sender_email, sender_password)

    print("Login successful")

    server.sendmail(sender_email, address_info, email_body_info)

    print("Message sent")

    entmail.delete(0, END)



but = Button(root, padx=2, pady=2, text='SIGN UP',
             command=lambda:[insert(), send_message()], font=('none 13 bold'))
but.place(x=60, y=140)

res = Button(root, padx=2, pady=2, text='LOGIN',
             command=show, font=('none 13 bold'))
res.place(x=200, y=140)


root.mainloop()
