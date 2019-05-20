import socket
import pickle

server_address = ('127.0.0.1',8081)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)


def printboard():
	print str(uboard[0])+ "|"+ str(uboard[1])+ "|"+ str(uboard[2])
	print "-"*5
	print str(uboard[3])+ "|"+ str(uboard[4])+ "|"+ str(uboard[5])
	print "-"*5
	print str(uboard[6])+ "|"+ str(uboard[7])+ "|"+ str(uboard[8])
	

state= "C"

begin=client_socket.recv(1024)
loadbegin= pickle.loads(begin)
uboard=loadbegin

printboard()

while True:
	if state == "B":
		piece=raw_input("piece>>")
		position=raw_input("position>>")

		message=[]
		message.append(piece)
		message.append(position)

		pmsg=pickle.dumps(message)

		client_socket.send(pmsg)
		state="A"
	elif state=="A":
		terima=client_socket.recv(1024)
		loadbegin= pickle.loads(terima)
		if terima.find("menang")!=-1:
			print "MENANG"
		else:
			uboard=loadbegin
			printboard()
		terima2=client_socket.recv(1024)
		loadbegin= pickle.loads(terima2)
		if terima2.find("menang")!=-1:
			print "MENANG"
		else:
			uboard=loadbegin
			printboard()
		state="B"
	elif state=="C":
		terima=client_socket.recv(1024)
		loadbegin= pickle.loads(terima)
		uboard=loadbegin
		printboard()
		state="B"

