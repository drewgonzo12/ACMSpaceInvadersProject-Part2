import pygame
from tkinter import *
from PIL import Image,ImageTk #python -m pip install pillow to cmd

def exit1():
        exit()

window = Tk()
window.geometry("460x600")
window.title("SPACE INVADERS!")

#this block of code MUST come after window = Tk(), not before----
imge1 = Image.open("C:/Users/elton/OneDrive/Desktop/SpaceInvaders/img/ast.png")
photo1 = ImageTk.PhotoImage(imge1)

lab1 = Label(image = photo1)
lab1.pack()

fn = StringVar()
#----

#label1 = Label(window, text = "SPACE INVADERS", fg = "blue", bg = "yellow", font = ("arial", 16, "bold"))
#label1.pack(fill = BOTH, pady = 2, padx = 2)

label2 = Label(window, text = "Username :", width = 15, font = ("arial", 10, "bold"))
label2.place(x = 80, y = 200)

e1 = Text(window, width=20, height=1, font = ("arial", 10, "bold"))
x = e1.get("1.0", "end-1c")
e1.insert("end", "")
e1.place(x = 240, y = 200)

#entry_1 = Entry(window, textvar = fn)
#entry_1.place(x = 240, y = 200)

label3 = Label(window, text = "Select Your Ship", width = 15, font = ("arial", 10, "bold"))
label3.place(x = 80, y = 255)

#ship selection
ship1photo = PhotoImage(file = "C:/Users/elton/OneDrive/Desktop/SpaceInvaders/img/shse1.png")
ship2photo = PhotoImage(file = "C:/Users/elton/OneDrive/Desktop/SpaceInvaders/img/shse2.png")
ship3photo = PhotoImage(file = "C:/Users/elton/OneDrive/Desktop/SpaceInvaders/img/shse3.png")

sop1 = Button(window, text = 'No powerups', image = ship1photo)
sop1.place(x = 94, y = 300)

sop2 = Button(window, text = 'Time stopper', image = ship2photo)
sop2.place(x = 197.5, y = 300)

sop3 = Button(window, text = 'Bullet dodger', image = ship3photo)
sop3.place(x = 310, y = 300)

label4 = Label(window, text = "Select Difficulty", width = 15, font = ("arial", 10, "bold"))
label4.place(x = 80, y = 390)

#buttons for controlling difficulty
b1 = Button(window, text = "easy", width = 12, bg = 'green', fg = 'papayawhip', command = print)
b1.place(x = 55, y = 445)

b2 = Button(window, text = "medium", width = 12, bg = '#ffcc00', fg = 'white', command = print)
b2.place(x = 180, y = 445)

b3 = Button(window, text = "hard", width = 12, bg = 'red', fg = 'papayawhip', command = print)
b3.place(x = 310, y = 445)

b4 = Button(window, text = "necessito exito", width = 12, bg = 'gray', fg = 'papayawhip', command = exit1)
b4.place(x = 180, y = 547)

window.mainloop()

