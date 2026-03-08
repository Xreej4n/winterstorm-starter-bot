import socket

host = "127.0.0.1"
port=6666

client_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_object.connect((host,port))

client_object.send("HELLO WORLD!".encode())
client_object.close()