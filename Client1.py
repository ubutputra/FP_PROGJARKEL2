import socket
import pickle

server_address = ('127.0.0.1',8081)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

state= "A"

begin=client_socket.recv(1024)
loadbegin= pickle.loads(begin)
uboard=loadbegin

printboard()

while True:
	if state == "A":
		piece=raw_input("piece>>")
		position=raw_input("position>>")
		message=[]
		message.append(piece)
		message.append(position)
		pmsg=pickle.dumps(message)
		client_socket.send(pmsg)
		state="B"
	elif state=="B":
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
		state="A"

