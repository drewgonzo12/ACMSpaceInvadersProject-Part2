import os
from tkinter import *
from PIL import Image,ImageTk #python -m pip install pillow to cmd

def exit1():
        exit()

#GUI.py is already implemented in BOSS.py, this seperate file is more for testing

window = Tk()
window.geometry("460x600")
window.title("SPACE INVADERS!")

# this block of code MUST come after window = Tk(), not before----
imge1 = Image.open(str(os.getcwd()) + "\\img\\ast.png")
photo1 = ImageTk.PhotoImage(imge1)

lab1 = Label(image=photo1)
lab1.pack()

label2 = Label(window, text="Username :", width=20, font=("arial", 10, "bold"))
label2.place(x=80, y=200)

e1 = Text(window, width=20, height=1, font=("arial", 10, "bold"))
x = e1.get("1.0", "end-1c")
e1.insert("end", "")
e1.place(x=240, y=200)

label3 = Label(window, text="Select Your Ship", width=20, font=("arial", 10, "bold"))
label3.place(x=80, y=255)

# ship selection
ship1photo = PhotoImage(file=str(os.getcwd()) + "\\img\\shse1.png")
ship2photo = PhotoImage(file=str(os.getcwd()) + "\\img\\shse2.png")
ship3photo = PhotoImage(file=str(os.getcwd()) + "\\img\\shse3.png")

sop1 = Button(window, text='Multi Shot', image=ship1photo, command=lambda: print)
sop1.place(x=94, y=300)

sop2 = Button(window, text='Invincibility', image=ship2photo, command=lambda: print)
sop2.place(x=197.5, y=300)

sop3 = Button(window, text='Za Warudo', image=ship3photo, command=lambda: print)
sop3.place(x=310, y=300)

label4 = Label(window, text="Select Difficulty", width=20, font=("arial", 10, "bold"))
label4.place(x=80, y=390)

# buttons for controlling difficulty
diff_1 = Button(window, text="EASY", width=12, bg='green', fg='papayawhip', command=lambda: print)
diff_1.place(x=55, y=445)

diff_2 = Button(window, text="MEDIUM", width=12, bg='#ffcc00', fg='white', command=lambda: print)
diff_2.place(x=180, y=445)

diff_3 = Button(window, text="HARD", width=12, bg='red', fg='papayawhip', command=lambda: print)
diff_3.place(x=310, y=445)

start = Button(window, text="Start game", width=12, bg='gray', fg='papayawhip', command=exit1)
start.place(x=180, y=550)


# buttons for controlling difficulty
diff_1 = Button(window, text="EASY", width=12, bg='green', fg='papayawhip', command=lambda: print)
diff_1.place(x=55, y=445)

diff_2 = Button(window, text="MEDIUM", width=12, bg='#ffcc00', fg='white', command=lambda: print)
diff_2.place(x=180, y=445)

diff_3 = Button(window, text="HARD", width=12, bg='red', fg='papayawhip', command=lambda: print)
diff_3.place(x=310, y=445)

start = Button(window, text="Start game", width=12, bg='gray', fg='papayawhip', command=exit1)
start.place(x=180, y=550)

window.mainloop()
