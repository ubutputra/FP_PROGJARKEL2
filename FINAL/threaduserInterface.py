import random
from Tkinter import *
from diceMove import dice
from PIL import Image, ImageTk
import time
import sys
import socket
import pickle
import threading
import select

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

class MatchPosition():
    def find_trap(self, block, turn, position):
        x = 35*(turn>=3)
        y = (turn%3)*35

        if(block == 4):
            return 1
        elif(block == 7):
            return 1
        elif(block == 15):
            return 1
        elif(block == 19):
            return 1
        elif(block == 24):
            return 1
        elif(block == 30):
            return 1
        elif(block == 35):
            return 1
        elif(block == 39):
            return 1
        elif(block == 46):
            return 1
        else:
            return 0

    def find_snake_or_ladder(self, block, turn, position):
        x = 35*(turn>=3)
        y = (turn%3)*35
        if(block == 17):
           return 455+x, 125+y, 36,0
        elif(block == 27):
            return 655+x, 25+y, 47,0
        elif(block == 44):
            return 265+x, 325+y, 18,0
        elif(block == 33):
            return 865+x, 325+y, 12,0
        elif(block == 38):
            return 465+x, 325+y, 16,0
        elif(block == 22):
            return 65+x, 25+y, 41,0

        elif(block == 4):
            return position[0], position[1], block,1
        elif(block == 7):
            return position[0], position[1], block,1
        elif(block == 15):
            return position[0], position[1], block,1
        elif(block == 19):
            return position[0], position[1], block,1
        elif(block == 24):
            return position[0], position[1], block,1
        elif(block == 30):
            return position[0], position[1], block,1
        elif(block == 35):
            return position[0], position[1], block,1
        elif(block == 39):
            return position[0], position[1], block,1
        elif(block == 46):
            return position[0], position[1], block,1
        else:
            return position[0], position[1], block,0
       
          
       



        # elif(block == 17):
        #    return 425+x, 510+y, 4
        # elif(block == 19):
        #    return 665+x, 390+y, 7
        # elif(block == 21):
        #    return 425+x, 390+y, 9
        # elif(block == 27):
        #    return 65+x, 510+y, 1
        # else:
        #     return position[0], position[1], block
        

class Display(object):
    def __init__(self,master,img):

        #Create board of snake and ladder
        canvas_width = 1200
        canvas_height = 700
        self.color = ["#FFF","#0F0", "#FF0", "#0FF"]
        self.canvas = Canvas(master, width = canvas_width, height = canvas_height, bg = "brown")
        self.canvas.grid(padx=0, pady=0)
        self.canvas.create_image(500,250,anchor=CENTER, image = img)


        #bahan-bahan
        self.x = 55
        self.y = 410
        self.m = []
        self.num_player = "Players"
        self.player = []
        self.position = []
        self.i = 0
        self.block=[]
        self.move = 1
        self.status = [20,20,20,20] #trap status
        self.turn = 0
        self.identity_player = 0
        self.gambar=[]
        image1=Image.open("image1.png").convert("RGBA")
        image2=Image.open("image2.png").convert("RGBA")
        image3=Image.open("image3.png").convert("RGBA")
        image4=Image.open("image4.png").convert("RGBA")
        self.begin= ''
        self.loadbegin=[]

        self.gambar.append(ImageTk.PhotoImage(image1))
        self.gambar.append(ImageTk.PhotoImage(image2))
        self.gambar.append(ImageTk.PhotoImage(image3))
        self.gambar.append(ImageTk.PhotoImage(image4))
        
        #CONNECTION
        self.server_address = ('127.0.0.1',8081)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        self.sockets_list = [self.client_socket]
        self.identity_player = self.client_socket.recv(1024)
        print "Player ke " + self.identity_player
        self.identity_player = int(self.identity_player)
        self.thread1=threading.Thread(target=self.cmdloop)
        self.thread1.start()
        

        #Drop Menu
        # OPTIONS = ["Players", "2", "3", "4"]
        # variable = StringVar(master)
        # variable.set(OPTIONS[0]) # default value
        # w = OptionMenu(self.canvas, variable, *OPTIONS, command=self.get_choice)
        # w.pack()
        # w.place(x=200, y=525)
        # w.config(font=('calibri',(10)),bg='white',width=5)
        
        #Start Game
        self.startGame = Button(self.canvas, text="Start Game", background='white', command = self.startGame, font=("Helvetica"))
        self.startGame.place(x=200, y=575)


    def startGame(self):
        self.diceRoll = Button(self.canvas, text="Roll",background='white', command = self.gamePlay, font=("Helvetica"))
        # testing = dice()
        # print "ROLL = " + str(testing)
        self.viewstat = Label(self.canvas, text="Player Status",background='white', font=("Helvetica"))

        if(self.identity_player==1):
            self.client_socket.send("START")
        #keterangan ->turn sekarang,jumlah player, roll turn sekarang, current player
        # self.begin = self.client_socket.recv(1024)
        # self.loadbegin= pickle.loads(self.begin)
        # #print self.loadbegin[0]
        # #print self.loadbegin[1]
        time.sleep(3)
        self.i = int(self.loadbegin[0])
        self.num_player = int(self.loadbegin[1])
        check = self.i%self.num_player
        nama = "Player " + str(self.identity_player)
        self.stat_value = Label(self.canvas, text=nama,background='white', font=("Helvetica", 25))
        print "identity_player: " + str(self.identity_player)
        if(check==self.identity_player-1):
            print "SEKARANG GILIRANMU"
        self.create_peice()
        self.startGame.place(x=-30, y=-30)
        #if((check+1)!=self.identity_player):
         #   self.diceRoll.place(x=-30,y=-30)
          #  self.viewstat.place(x=-90,y=-30)
            #self.begin = self.client_socket.recv(1024)
            #self.loadbegin= pickle.loads(self.begin)
           # self.i = self.loadbegin[0]
            #self.move = int(self.loadbegin[2])
            #print "MOVE = " + str(self.move)
            #print "MOVE = " + str(self.loadbegin[2])
            #check = self.i%self.num_player
            #turn = (self.i-1)%self.num_player
            #print "TURN = " +str(turn)
            #self.position[turn] = self.diceMove(self.position[turn], turn)
        #self.diceRoll.place(x=200, y=560)
        if(check!=self.identity_player-1):
            self.diceRoll.place(x=-30,y=-30)
        else:
            self.diceRoll.place(x=200,y=560)
        self.viewstat.place(x=100, y=560)
        self.stat_value.place(x=400,y=560)


    def get_choice(self, value):
        self.num_player = value


    def diceMove(self, position, turn):
        # move = dice()

        #move = 1
        #Print Dice Value to screen
        dice_value = Label(self.canvas, text=str(self.move),
                           background='white', font=("Helvetica", 25))
        dice_value.pack()
        dice_value.place(x=205, y=605)

        stat_value = Label(self.canvas, text=str(self.status[turn]),
                           background='white', font=("Helvetica", 25))
        stat_value.pack()
        stat_value.place(x=105, y=605)
        
        turn_info = 'Player ' + str(turn+1)
        turn_value = Label(self.canvas, text=turn_info,
                           background='white', font=("Helvetica", 20))
        turn_value.pack()
        turn_value.place(x=265, y=585)
        
        self.x, self.y = position[0], position[1]
        if(self.move+self.block[turn] > 50):
            return [self.x, self.y]
        
        #self.move = move
        self.block[turn] += self.move
        
        self.canvas.delete(self.player[turn])
        self.peices(turn)

        return [self.x, self.y]
        
    def peices(self, turn):
       #gerak pion
        for i in range(self.move,0,-1):
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
        self.x, self.y, self.block[turn],checktrap= MatchPosition().find_snake_or_ladder(self.block[turn], turn, [self.x, self.y])
        if checktrap==1:
            self.status[turn] -= 10
            if self.status[turn] <= 0:
                self.status = 50
                self.x = 55
                self.y = 410
                self.block[turn] = 1
                self.canvas.delete(self.player[turn])
                #self.player[turn] = self.canvas.create_circle(self.x, self.y, 15, fill=self.color[turn], outline="")
                self.player[turn]=self.canvas.create_image(self.x,self.y,anchor=CENTER, image = self.gambar[turn])

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
        # print "SELF I = " + str(self.i)
        # check = self.i%self.num_player
        # print "CHECK = " + str(check) + "PLAYER = " + str(self.identity_player)
        # if(check!=self.identity_player-1):
        #     self.i = int(self.loadbegin[0])
        #     self.move = int(self.loadbegin[2])
        #     check = self.i%self.num_player
        #     turn = (self.i-1)%self.num_player
        #     if (self.i!=0 and turn!=self.identity_player-1 and self.loadbegin[2]!=0):
        #         self.position[turn] = self.diceMove(self.position[turn], turn)
        #         self.loadbegin[2]=0
        #         print "UPDATED"
        #     else:
        #         print "UPDATING"
        # else:
        #keterangan ->turn sekarang,jumlah player, roll turn sekarang, current player
        for iterator in range(self.num_player):
            print "I senilai = " + str(iterator)
            if iterator != self.identity_player-1:
                print str(iterator)
                self.move=self.loadbegin[4][iterator]
                self.position[iterator]=self.diceMove(self.position[iterator], iterator)
                if(self.block[iterator] >= 50):
                    self.diceRoll.place(x=-30, y=-30)
                    print("Won", iterator+1)
                    top = Toplevel()
                    top.title("Snake and Ladder")
                    message = "Player " + str(iterator+1) + " Won" 
                    msg = Message(top, text=message)
                    top.geometry("%dx%d%+d%+d" % (100, 100, 250, 125))
                    msg.pack()
                    button = Button(top, text="Dismiss", command=top.destroy)
                    button.pack()
            else:
                self.client_socket.send(str(self.identity_player))
                time.sleep(0.5)
                self.i = int(self.loadbegin[0])
                self.move = int(self.loadbegin[2])
                check = self.i%self.identity_player
                turn = (self.i-1)%self.num_player
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
    def cmdloop(self):
        while 1:
            sys.stdout.flush()
            # Wait for input from stdin & socket
            inputs, outputs, excepts = select.select(self.sockets_list,[],[],1)

            for abc in inputs:
                if abc == self.client_socket:
                    self.begin = self.client_socket.recv(1024)
                    self.loadbegin= pickle.loads(self.begin)
                    #keterangan ->turn sekarang,jumlah player, roll turn sekarang, current player
                    self.i = int(self.loadbegin[0])
                    self.num_player = int(self.loadbegin[1])
                    check = self.i % self.num_player
                    if(check!=self.identity_player-1 and self.i!=0):
                        self.diceRoll.place(x=-30,y=-30)
                    elif(check==self.identity_player-1 and self.i!=0):
                        self.diceRoll.place(x=200,y=560)
        #master.after(500,cmdloop)        
            
 
    # def trap_status(self,poin):
    #     status_value= Label(self.canvas, text=str(self.status),
    #                        background='white', font=("Helvetica", 25))
    #     status_value.pack()
    #     status_value.place(x=255, y=605)