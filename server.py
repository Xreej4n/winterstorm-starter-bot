import socket
host = ""
port = 6666


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host,port))

server_socket.listen(2)
print("Server waiting for message...")

connObj, addr = server_socket.accept()
print(f"Connection accepted from {addr}")

message = connObj.recv(1024).decode()
print(f"Received message:\n{message}")

connObj.close()
server_socket.close()