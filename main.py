from userInterface import *
        
def main():
    master = Tk()
    master.title("Snake and Ladder HOST")
    master.geometry("1400x800")
    img = PhotoImage( file = "board2.1.gif")
    game = Display(master,img)
    master.mainloop()

main()
 