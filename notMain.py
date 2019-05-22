from userInterface2 import *
        
def notmain():
    master = Tk()
    master.title("Snake and Ladder NOT HOST")
    master.geometry("1400x800")
    img = PhotoImage( file = "board2.gif")
    game = Display(master,img)
    master.mainloop()

notmain()
