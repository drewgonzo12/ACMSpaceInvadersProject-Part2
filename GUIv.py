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
#----

#label1 = Label(window, text = "SPACE INVADERS", fg = "blue", bg = "yellow", font = ("arial", 16, "bold"))
#label1.pack(fill = BOTH, pady = 2, padx = 2)

label2 = Label(window, text = "Username :", width = 20, font = ("arial", 10, "bold"))
label2.place(x = 80, y = 200)

label3 = Label(window, text = "Select Your Ship", width = 20, font = ("arial", 10, "bold"))
label3.place(x = 80, y = 255)

label4 = Label(window, text = "Select Difficulty", width = 20, font = ("arial", 10, "bold"))
label4.place(x = 80, y = 325)

b1 = Button(window, text = "easy", width = 12, bg = 'green', fg = 'papayawhip', command = print)
b1.place(x = 55, y = 400)

b2 = Button(window, text = "medium", width = 12, bg = '#ffcc00', fg = 'white', command = print)
b2.place(x = 180, y = 400)

b3 = Button(window, text = "hard", width = 12, bg = 'red', fg = 'papayawhip', command = print)
b3.place(x = 310, y = 400)

b4 = Button(window, text = "necessito exito", width = 12, bg = 'gray', fg = 'papayawhip', command = exit1)
b4.place(x = 180, y = 550)

window.mainloop()

