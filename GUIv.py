# import the modules  
import math
import tkinter 
import random 

score = 0

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (112, 118, 123)
YELLOW = (255, 255, 0)
  
# the game time left, initially 30 seconds. 
timeleft = 30
  
# function that will start the game. 
def startGame(event): 
          
        # update the score. 
        scoreLabel.config(text = "Score: " + str(score)) 
  
class Score(object):
	def __init__(self, name):
		self.name = name
  
# create a GUI window 
root = tkinter.Tk() 
  
# set the title 
root.title("SPACE INVADERS!") 
  
# set the size 
root.geometry("460x600") 
  
# add an instructions label 
instructions = tkinter.Label(root, text = "Arrow keys to move, "
                        "Space to fire weapon", 
                                      font = ('Courier', 12)) 
instructions.pack()  

v = tkinter.IntVar()

tkinter.Label(root, 
        text="""Select your ship, 1 or 2""",
        justify = tkinter.LEFT,
        padx = 20).pack()

tkinter.Radiobutton(root, 
              text="Rigel Axiom",
              padx = 20, 
              variable=v, 
              value=1).pack(anchor=tkinter.W)

tkinter.Radiobutton(root, 
              text="Voyager II",
              padx = 20, 
              variable=v, 
              value=2).pack(anchor=tkinter.W)

# add a score label 
scoreLabel = tkinter.Label(root, text = "Score Tracker: ", 
                                      font = ('Courier', 12)) 
scoreLabel.pack() 
  
# start the GUI 
root.mainloop() 