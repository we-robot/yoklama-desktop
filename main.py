# coding=utf-8

from tkinter import *
import cv2
from PIL import Image, ImageTk

width, height = 600, 300
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

master = Tk()
master.minsize(800,600)
master.geometry("820x600")
master.configure(background='#3498db')

def btn_webcam_click():
    print("webcamm acildi!")
    for widget in panel.winfo_children():
        widget.destroy()
    camera = Label(panel)
    camera.pack()


    def btn_fotograf_cek_click():
        camera2 = Label(panel)
        camera2.pack()
        print("fotograf çekildi")
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imwrite('cam.jpg',frame)
        for widget in panel.winfo_children():
            widget.destroy()
        camera2 = Label(panel)
        camera2.pack()
        image = ImageTk.PhotoImage(Image.open("cam.jpg"))
        camera2.imgtk = image
        camera2.configure(image=image)

        def btn_kaydet_click():
            #Veritabanına Eklenecek
            print("erferf")

        btn_kaydet = Button(panel, text="Kaydet", command=btn_kaydet_click)
        btn_kaydet.place(height = 50, width=150, y=380, x=230)


    btn_fotograf_cek = Button(panel, text="Yoklama Al", command=btn_fotograf_cek_click)
    btn_fotograf_cek.place(height = 50, width=150, y=380, x=230)


    def show_frame():

        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        camera.imgtk = imgtk
        camera.configure(image=imgtk)
        camera.after(10, show_frame)

    show_frame()

def btn_new_person_click():
    print("yeni kişi a癟覺ld覺")

def btn_show_people_click():
    print("ki��i listesi a癟覺ld覺")

def btn_quit_click():
    print("ki��i listesi a癟覺ld覺")

btn_webcam = Button(master, text="Yoklama Al", command=btn_webcam_click,
                    compound=LEFT, background='#ecf0f1', relief=FLAT,
                    cursor="hand1", activebackground='#3498db')
btn_webcam.place(x = 20, y = 20, height=50, width=150)



btn_new_person = Button(master, text="Kişi Ekle", command=btn_new_person_click,
                        compound=LEFT, background='#ecf0f1', relief=FLAT,
                        cursor="hand1", activebackground='#3498db')
btn_new_person.place(x = 20, y = 90, height=50, width=150)


btn_show_people = Button(master, text="Kişi Listesi", command=btn_show_people_click,
                         compound=LEFT, background='#ecf0f1', relief=FLAT,
                         cursor="hand1", activebackground='#3498db')
btn_show_people.place(x = 20, y = 160, height=50, width=150)


btn_quit = Button(master, text="Çıkış", command=btn_quit_click, cursor="hand1",
                  compound=LEFT, background='#ecf0f1', relief=FLAT,
                  activebackground='#3498db')
btn_quit.place(x = 20, y = 230, height=50, width=150)

panel = Frame(master, relief=RAISED, borderwidth=1, background='#2980b9')
panel.place(x = 190, y = 20, height=560, width=610)







mainloop()
