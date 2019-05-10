#from tkinter import *
from Tkinter import *

def close_window(): 
    window.destroy()

window = Tk()
 
window.title("Snake And Ladder Game Multiplayer")
window.geometry('350x200')
lbl = Label(window, text="Snake And Ladder Game", font=("Arial Bold", 20))
 
lbl.grid(column=0, row=0)

btn = Button(window, text="Play")
btn.grid(column=0, row=1) 

btn = Button(window, text="Exit",command=close_window)
btn.grid(column=0, row=3) 



window.mainloop()
