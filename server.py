from socket import AF_INET, socket, SOCK_STREAM
import threading
from threading import Thread

###################################### Global variables #####################################
clients = {}
addresses = {}

##################################### Defining Host and Server ##################################
HOST = 'localhost'
PORT = 52346
BUFSIZE = 1024
ADDRESS = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

######################################## Functions ##############################################
def listen():
    print("Waiting for connection...")
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to the Chatbot!" + "    " + "Please enter your name here : ", "utf8"))
        addresses[client] = client_address
        Thread(target = listentoclient, args = (client,)).start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")


def listentoclient(client):
    name = client.recv(BUFSIZE).decode("utf8")
    message = "Welcome to the Chatbot %s To exit please type {QUIT}" % name
    client.send(bytes(message, "utf8"))
    msg = "%s joined the chatroom" % name
    sendMessage(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZE)
        if msg != bytes("{QUIT}", "utf8"):
            sendMessage(msg, name+": ")
        else:
            client.send(bytes("{QUIT}", "utf8"))
            client.close()
            del clients[client]
            break


def sendMessage(msg, name=""):
	for client in clients:
		client.send(bytes(name, "utf8") + msg)



if __name__ == "__main__":
	SERVER.listen(5)	#Maximum 5 connections
	ACCEPT_THREAD = Thread(target=listen)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()