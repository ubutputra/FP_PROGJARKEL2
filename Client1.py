import socket
import pickle

server_address = ('127.0.0.1',8081)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)



#keterangan ->turn sekarang,jumlah player, roll turn sekarang, posisi player 1, posisi player 2, posisi player 3, posisi player 4
#keterangan=[turnnow,jumlah_player,roll,posisi_1,posisi_2,posisi_3,posisi_4]

def printdata():
	print "Turn Sekarang = " + str(data[0])
	print "-"*5
	print "Jumlah Player = " + str(data[1])
	print "-"*5
	print "Roll Player Sekarang = " + str(data[2])
	print "-"*5
	print "Posisi Player 1 = " + str(data[3])
	print "-"*5
	print "Posisi Player 2 = " + str(data[4])
	print "-"*5
	print "Posisi Player 3 = " + str(data[5])
	print "-"*5
	print "Posisi Player 4 = " + str(data[6])
	print "-"*5

state= "A"
begin=client_socket.recv(1024)
loadbegin= pickle.loads(begin)
data=loadbegin
printdata()
start=raw_input("Mulai? Ketik Ya Untuk Mulai>>")
client_socket.send(start)

while True:
	if state == "A":
		roll=raw_input("roll>>")
		rollString=str(roll)
		print rollString
		client_socket.send(rollString)
		state="B"
	elif state=="B":
		terima=client_socket.recv(1024)
		loadbegin= pickle.loads(terima)
		if terima.find("menang")!=-1:
			print "MENANG"
		else:
			data=loadbegin
			printdata()
		state="A"

