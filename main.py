# coding=utf-8

from tkinter import *
import cv2
from PIL import Image, ImageTk
import requests
import time
from tkinter import messagebox as mbox
from tkinter.ttk import Combobox
a = 0
width, height = 800, 600

cap = cv2.VideoCapture()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

number = -1
master = Tk()
master.minsize(800,600)
master.geometry("820x600")
master.configure(background='#3498db')

def btn_webcam_click():
    global a
    
    if(a == 1):
        print("webcamm acildi!")
    else:
        a = 1
        
        global cap   
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        for widget in panel.winfo_children():
            widget.destroy()
        camera = Label(panel)
        camera.pack()

        r = requests.get("http://localhost:3000/lessons/")
        cmbDersler = Combobox(panel,values=r.json())

        cmbDersler.set("Ders Seçiniz")
        cmbDersler.place(height=20, width=150, y=400,x=230)

        def btn_fotograf_cek_click():
            number = cmbDersler.current()
            if number == -1:
                mbox.showinfo("Hata", "Ders Secmediniz")

            else:
                print("fotograf çekildi")
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                cv2.imwrite('cam.jpg',frame)
                cap.release()
                for widget in panel.winfo_children():
                    widget.destroy()
                camera2 = Label(panel)
                camera2.pack()
                image = ImageTk.PhotoImage(Image.open("cam.jpg"))
                camera2.imgtk = image
                camera2.configure(image=image)
                global a
                a = 0
                def btn_kaydet_click():

                    # mbox.showinfo("Hata", "Ders Secmediniz"+number)
                    #Veritabanına Eklenecek
                    
                    files = {'image': open('cam.jpg', 'rb')}
                    r = requests.post("http://localhost:3000/inspections/",{ 'lesson_number': number }, files=files)
                    mbox.showinfo("Yoklama Gönderildi", r.json()['message'])
                    for widget in panel.winfo_children():
                        widget.destroy()

                    global a
                    a = 0

                btn_kaydet = Button(panel, text="Kaydet", command=btn_kaydet_click)
                btn_kaydet.place(height = 50, width=150, y=400, x=230)


        btn_fotograf_cek = Button(panel, text="Yoklama Al", command=btn_fotograf_cek_click)
        btn_fotograf_cek.place(height = 50, width=150, y=430, x=230)


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
    global a
    a = 0
    global cap
    cap.release()
    cv2.destroyAllWindows()
    print("yeni kişi menüsü açıldı")
    for widget in panel.winfo_children():
        widget.destroy()

    lbl_ad = Label(panel, text="Aldığı Dersler :", anchor='w',
                         bg='#ecf0f1')
    lbl_ad.place(height = 20, width=200, y=140, x=20)
        
    r = requests.get("http://localhost:3000/lessons/")
    l = Listbox(panel, selectmode= EXTENDED)
    values = r.json()
    for value in values:
        l.insert(END, value)
        
    l.place(height = 200,width = 200, y = 140, x = 220)

    lbl_ad = Label(panel, text="Ad :", anchor='w',
                         bg='#ecf0f1')
    lbl_ad.place(height = 20, width=200, y=20, x=20)

    txt_ad = Entry(panel)
    txt_ad.place(height = 20, width=200, y=20, x=220)

    lbl_soyad = Label(panel, text="Soyad :", anchor='w',
                         bg='#ecf0f1')
    lbl_soyad.place(height = 20, width=200, y=60, x=20)

    txt_soyad = Entry(panel)
    txt_soyad.place(height = 20, width=200, y=60, x=220)

    lbl_numara = Label(panel, text="Numara:", anchor='w',
                         bg='#ecf0f1')
    lbl_numara.place(height = 20, width=200, y=100, x=20)

    txt_numara = Entry(panel)
    txt_numara.place(height = 20, width=200, y=100, x=220)
    def btn_ekle_click():
        items = l.curselection()
        ad = txt_ad.get()
        soyad = txt_soyad.get()
        numara = txt_numara.get()
        dersler = ((str(e) + " ") for e in items)
        r = requests.post("http://localhost:3000/students/", data={"name": ad,"surname":soyad,"number": numara, "lessons": "".join(dersler)})
        mbox.showinfo("Kişi Eklendi", r.json()['message'])
    btn_ekle = Button(panel, command=btn_ekle_click, text="Ekle")
    btn_ekle.place(height=40, width=200, y=360, x=220)


def btn_show_people_click():
    global a
    a = 0
    global cap
    cap.release()
    cv2.destroyAllWindows()
    for widget in panel.winfo_children():
        widget.destroy()
    r = requests.get("http://localhost:3000/students/")
    students = r.json()
    for student in students:
        entryText = StringVar()
        hucre = Entry(panel, text="", textvariable=entryText)
        hucre.grid(row=student["id"], column=0)
        entryText.set(student["id"])

        entryText2 = StringVar()
        hucre = Entry(panel, text="", textvariable=entryText2)
        hucre.grid(row=student["id"], column=1)
        entryText2.set(student["name"])

        entryText3 = StringVar()
        hucre = Entry(panel, text="", textvariable=entryText3)
        hucre.grid(row=student["id"], column=2)
        entryText3.set(student["surname"])


        entryText4 = StringVar()
        hucre = Entry(panel, text="", textvariable=entryText4)
        hucre.grid(row=student["id"], column=3)
        entryText4.set(student["number"])


def btn_show_yoklama_click():

    global a
    a = 0
    global cap
    cap.release()
    cv2.destroyAllWindows()
    for widget in panel.winfo_children():
        widget.destroy()
    panel2 = Frame(panel, relief=RAISED)
    panel2.place(x = 20, y = 60)
    def btn_yoklama_goster_click():
        r = requests.post("http://localhost:3000/inspections/list", data={
            "gun": cmbGun.get(),
            "ay": cmbAy.get(),
            "yil": cmbYil.get(),
            "ders_id": cmbDersler.current()
        })
        

        for widget in panel2.winfo_children():
            widget.destroy()
        students = r.json()['message']
        sayac2 = 0
        
        for student in students:
            sayac2 += 1
            entryText3 = StringVar()
            hucre = Entry(panel2, text="", textvariable=entryText3)
            hucre.grid(row=sayac2, column=1)
            entryText3.set(student["name"])


            entryText4 = StringVar()
            hucre = Entry(panel2, text="", textvariable=entryText4)
            hucre.grid(row=sayac2, column=2)
            entryText4.set(str(student["number"]))
        

    r = requests.get("http://localhost:3000/lessons/")
    cmbDersler = Combobox(panel,values=r.json())
    cmbDersler.set("Ders Seçiniz")
    cmbDersler.place(height=20, width=150, y=20, x=30)
    
    cmbGun = Combobox(panel,values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,25,26,27,28,29,30,31])
    cmbGun.set("Gün")
    cmbGun.place(height=20, width=50, y=20, x=210)
    
    cmbAy = Combobox(panel,values=[1,2,3,4,5,6,7,8,9,10,11,12])
    cmbAy.set("Ay")
    cmbAy.place(height=20, width=50, y=20, x=270)

    cmbYil = Combobox(panel, values=[2018, 2019])
    cmbYil.set("Yıl")
    cmbYil.place(height=20, width=50, y=20, x=330)

    btn_göster = Button(panel, command=btn_yoklama_goster_click, text="Göster")

    btn_göster.place(height=20, width=150, y=20, x=400)

def btn_quit_click():
    global a
    a = 0
    global cap
    cap.release()
    cv2.destroyAllWindows()
    print("çıkış butonu tıklandı")

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



btn_show_yoklama = Button(master, text="Yoklama", command=btn_show_yoklama_click,
                         compound=LEFT, background='#ecf0f1', relief=FLAT,
                         cursor="hand1", activebackground='#3498db')
btn_show_yoklama.place(x = 20, y = 230, height=50, width=150)


btn_quit = Button(master, text="Çıkış", command=btn_quit_click, cursor="hand1",
                  compound=LEFT, background='#ecf0f1', relief=FLAT,
                  activebackground='#3498db')
btn_quit.place(x = 20, y = 300, height=50, width=150)

panel = Frame(master, relief=RAISED, borderwidth=1, background='#2980b9')
panel.place(x = 190, y = 20, height=560, width=610)

mainloop()