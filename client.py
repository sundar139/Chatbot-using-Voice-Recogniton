from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import speech_recognition as sr
from gtts import gTTS

################################## Functions to be used ####################################

def receiveMessage():
	while True:
		try:
			msg = client_socket.recv(BUFSIZ).decode("utf8")
			msgList.insert(tkinter.END, msg)
		except OSError:	 #If the client leaves the chat
			break


def sendMessage(event = None):
	msg = message.get()
	message.set("")
	client_socket.send(bytes(msg, "utf8"))
	if msg == "{QUIT}":
		client_socket.close()
		top.quit()


def closeWindow(event = None):
	message.set("{QUIT}")
	sendMessage()

##################################### Voice to Text Function #################################

def voiceMessage(event = None):

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)
        print('Say something: ')
        audio = r.listen(source)
        voice_data = r.recognize_google(audio)
        print(voice_data)

    msg = voice_data  
    client_socket.send(bytes(msg, "utf8"))  
    if msg == "{QUIT}":
        client_socket.close()
        top.quit()
    
####################################### Creating The GUI and it's layout ##################################
top = tkinter.Tk()
top.title("Chatbot")
top.geometry("630x500+0+0")
top.config(bg="#154360")

frame = tkinter.Frame(top)

message = tkinter.StringVar()

scrollbar = tkinter.Scrollbar(frame, bg="#5B2C6F")
msgList = tkinter.Listbox(frame, height=25, width=100, yscrollcommand=scrollbar.set, bg="#5B2C6F", fg="white")

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msgList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msgList.pack()

frame.pack(pady=20)


entry_field = tkinter.Entry(top, width=40, textvariable=message, bg="#4A235A", fg="white" )
entry_field.bind("<Return>", sendMessage)
send_button = tkinter.Button(top, text="Send", command=sendMessage, highlightbackground="#000000", width=10)
voice_button = tkinter.Button(top, text="Voice", command=voiceMessage, highlightbackground="#000000", width=10)
entry_field.pack(side=tkinter.LEFT, padx=(220,10))
entry_field.config(highlightbackground="black")
send_button.pack(side=tkinter.LEFT,fill=tkinter.X)
voice_button.pack(side=tkinter.LEFT,fill=tkinter.X)

#################################### Creating INPUT Field #######################################
top.protocol("WM_DELETE_WINDOW", closeWindow)

HOST = "127.0.0.1"
PORT = 52346

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

################################### Beginning the Thread ####################################
receive_thread = Thread(target=receiveMessage)
receive_thread.start()
tkinter.mainloop()
