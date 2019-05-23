import pickle
import select
import socket
import sys
from diceMove import *

from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

IP_ADDRESS = "127.0.0.1"

Port = 8081

server.bind((IP_ADDRESS,Port))

server.listen(100)

list_of_clients=[]

#A1=1 A2=2 A3=3 B1=4 B2=5 B3=6


movehistory= [0,0,0,0]
turnnow = 0
jumlah_player = 0
curr_player = 0
roll = 0
#keterangan ->turn sekarang,jumlah player, roll turn sekarang, current player
keterangan=[turnnow,jumlah_player,roll,curr_player]
keterangandump=pickle.dumps(keterangan)

#state A -> game belum mulai, state B -> game sudah mulai
state ="A"

def clientthread(conn,addr):
	while True:
		global state
		global turnnow
		global jumlah_player
		global roll
		global curr_player
		global keterangan
		global keterangandump
		global movehistory
		try:
			message=conn.recv(2048)
			if message:
				if state == "A":
					state = "B"
					print "Game Mulai"
					keterangan=[turnnow,jumlah_player,roll,curr_player]
					keterangandump=pickle.dumps(keterangan)
					broadcast(keterangandump,conn)
				else:
					messageload = pickle.loads(message)
					curr_player=int(messageload[0])
					prime_power = int(messageload[1])
					print "PLAYER :" + str(curr_player)
					print "PRIME POWER: " + str(prime_power)
					if prime_power == 1:
						roll = dicePrime()
					elif prime_power == 2:
						roll = diceNotPrime()
					elif prime_power == 0:
						roll = dice()					
					movehistory[curr_player-1]=roll

					turnnow+=1
					print "TURN = + " + str(turnnow)
					print "ROLL = + " + str(roll)
					keterangan=[turnnow,jumlah_player,roll,curr_player,movehistory]
					keterangandump=pickle.dumps(keterangan)
					broadcast(keterangandump,conn)
			else:
				remove(conn)
		except:
			continue

def broadcast(message,connection):
	for clients in list_of_clients:
		clients.send(message)

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	conn,addr = server.accept()
	list_of_clients.append(conn)
	jumlah_player +=1
	# keterangan=[turnnow,jumlah_player,roll,posisi_1,posisi_2,posisi_3,posisi_4]
	# keterangandump=pickle.dumps(keterangan)
	conn.send(str(jumlah_player))
	print addr[0] + "connected"
	start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()