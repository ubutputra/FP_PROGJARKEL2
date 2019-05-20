import pickle
import select
import socket
import sys

from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

IP_ADDRESS = "127.0.0.1"

Port = 8081

server.bind((IP_ADDRESS,Port))

server.listen(100)

list_of_clients=[]

#A1=1 A2=2 A3=3 B1=4 B2=5 B3=6

turnnow = 0
jumlah_player = 0
posisi_1 = 0
posisi_2 = 0
posisi_3 = 0
posisi_4 = 0
roll = 0
#keterangan ->turn sekarang,jumlah player, roll turn sekarang, posisi player 1, posisi player 2, posisi player 3, posisi player 4
keterangan=[turnnow,jumlah_player,roll,posisi_1,posisi_2,posisi_3,posisi_4]
keterangandump=pickle.dumps(keterangan)


def clientthread(conn,addr):
	while True:
		try:
			message=conn.recv(2048)
			if message:
				dapat=pickle.loads(message)
				else:	
					print "<" + addr[0] + "> " 
					boarddump=pickle.dumps(board)
					broadcast(boarddump,conn)
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
	keterangan=[turnnow,jumlah_player,roll,posisi_1,posisi_2,posisi_3,posisi_4]
	keterangandump=pickle.dumps(keterangan)
	conn.send(keterangandump)
	print addr[0] + "connected"
	start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()