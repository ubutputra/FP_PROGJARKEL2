import random
from Tkinter import *
from diceMove import dice
import time

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

class MatchPosition():
    def find_snake_or_ladder(self, block, turn, position):
        x = 35*(turn>=3)
        y = (turn%3)*35
        if(block == 17):
           return 455+x, 125+y, 36
        elif(block == 27):
            return 655+x, 25+y, 47
        elif(block == 44):
            return 265+x, 325+y, 18
        elif(block == 33):
            return 865+x, 325+y, 12
        # elif(block == 17):
        #    return 425+x, 510+y, 4
        # elif(block == 19):
        #    return 665+x, 390+y, 7
        # elif(block == 21):
        #    return 425+x, 390+y, 9
        # elif(block == 27):
        #    return 65+x, 510+y, 1
        else:
            return position[0], position[1], block
        

class Display(object):
    def __init__(self,master,img):

        #Create board of snake and ladder
        canvas_width = 1200
        canvas_height = 700
        self.color = ["#FFF","#0F0", "#FF0", "#0FF"]
        self.canvas = Canvas(master, width = canvas_width, height = canvas_height, bg = "brown")
        self.canvas.grid(padx=0, pady=0)
        self.canvas.create_image(500,250,anchor=CENTER, image = img)

        self.x = 55
        self.y = 410
        self.m = []
        self.num_player = "Players"
        self.player = []
        self.position = []
        self.i = 0
        self.block=[]
        self.move = 1
        self.turn = 0
        self.gambar=[]
        self.gambar.append(PhotoImage( file = "image1.gif"))
        self.gambar.append(PhotoImage( file = "image2.gif"))
        self.gambar.append(PhotoImage( file = "image3.gif"))
        self.gambar.append(PhotoImage( file = "image4.gif"))
        self.act=0
        
        #Drop Menu
        OPTIONS = ["Players", "2", "3", "4"]
        variable = StringVar(master)
        variable.set(OPTIONS[0]) # default value
        w = OptionMenu(self.canvas, variable, *OPTIONS, command=self.get_choice)
        w.pack()
        w.place(x=200, y=525)
        w.config(font=('calibri',(10)),bg='white',width=5)
        
        #Start Game
        self.startGame = Button(self.canvas, text="Start", background='white', command = self.startGame, font=("Helvetica"))
        self.startGame.place(x=200, y=575)


    def startGame(self):
        if(self.num_player == "Players"):
            pass
        else:
            #Dice
            #Screen
            # self.canvas.create_rectangle(810, 150, 1160, 100, fill='white', outline='black')
            # self.canvas.pack(fill=BOTH, expand=1)
            #Button
            self.diceRoll = Button(self.canvas, text="Roll",background='white',
                                   command = self.gamePlay, font=("Helvetica"))
            self.num_player = int(self.num_player)
            self.diceRoll.place(x=200, y=560)
            self.create_peice()
            self.startGame.place(x=-30, y=-30)


    def get_choice(self, value):
        self.num_player = value


    def diceMove(self, position, turn):
        move = dice()

        #move = 1
        #Print Dice Value to screen
        dice_value = Label(self.canvas, text=str(move),
                           background='white', font=("Helvetica", 25))
        dice_value.pack()
        dice_value.place(x=205, y=605)
        
        turn_info = 'Player ' + str(turn+1)
        turn_value = Label(self.canvas, text=turn_info,
                           background='white', font=("Helvetica", 20))
        turn_value.pack()
        turn_value.place(x=265, y=585)
        
        self.x, self.y = position[0], position[1]
        if(move+self.block[turn] > 50):
            return [self.x, self.y]
        
        self.move = move
        self.block[turn] += move
        
        self.canvas.delete(self.player[turn])
        self.peices(move, turn)

        return [self.x, self.y]
        
    def peices(self, move, turn):
       #gerak pion
        for i in range(move,0,-1):
            self.x = self.x+100*self.m[turn]

            if(self.x>955 and turn < 4):
                self.y = self.y - 100
                self.x = 955
                self.m[turn] = -1
                print "pertama"
            elif(self.x>1000 and turn >=4):
                self.y = self.y - 100
                self.x = 1000
                self.m[turn] = -1
                print "kedua"
            if(self.x<55 and turn < 4):
                self.x = 55
                self.y -= 100
                self.m[turn] = 1
                print "ketiga"
            elif(self.x<100 and turn >=4):
                self.x = 100
                self.y -= 100
                self.m[turn] = 1
                print "keempat" 
            if(self.y<55):
                self.y=55
                print "last"

            # Code For the Animation of piece
            self.canvas.delete(self.player[turn])
            #self.player[turn] = self.canvas.create_circle(self.x, self.y, 15, fill=self.color[turn], outline=self.color[turn])
            self.player[turn]=self.canvas.create_image(self.x,self.y,anchor=CENTER, image = self.gambar[turn])
            self.canvas.update()
            time.sleep(0.25)

            
        print(self.x, self.y, self.block[turn])
        if self.block[turn]==44:
            self.m[turn]= -1
        self.x, self.y, self.block[turn] = MatchPosition().find_snake_or_ladder(self.block[turn], turn, [self.x, self.y])
        
        # if(any(self.y == ai for ai in [390, 425, 460, 150, 185, 220])):
        #     print "wat "+str(ai)
        #     self.m[turn] = -1
        # else:
        #     self.m[turn] = 1
        #     print "nani"
        print(self.x,self.y, self.block[turn])
        self.canvas.delete(self.player[turn])
        #self.player[turn] = self.canvas.create_circle(self.x, self.y, 15, fill=self.color[turn], outline="")
        self.player[turn]=self.canvas.create_image(self.x,self.y,anchor=CENTER, image = self.gambar[turn])


    def create_peice(self):
        for i in range(int(self.num_player)):
            #self.player.append(self.canvas.create_circle(self.x, self.y, 15, fill=self.color[i], outline=""))
            self.player.append(self.canvas.create_image(self.x,self.y,anchor=CENTER, image = self.gambar[i]))
            self.position.append([self.x, self.y])
            self.m.append(1)
            self.block.append(1)
            self.y += 20


    def gamePlay(self):
        turn = self.i%self.num_player
        self.i += 1
        self.turn = turn
        self.position[turn] = self.diceMove(self.position[turn], turn)
        if(self.block[self.turn] >= 50):
            self.diceRoll.place(x=-30, y=-30)
            print("Won", self.turn+1)
            top = Toplevel()
            top.title("Snake and Ladder")
            message = "Player " + str(self.turn+1) + " Won" 
            msg = Message(top, text=message)
            top.geometry("%dx%d%+d%+d" % (100, 100, 250, 125))
            msg.pack()
            button = Button(top, text="Dismiss", command=top.destroy)
            button.pack()
            
 
