from userInterface import *
        
def main():
    master = Tk()
    master.title("Snake and Ladder")
    master.geometry("1400x800")
    img = PhotoImage( file = "board2.gif")
    x = Display(master,img)
    master.mainloop()

main()
