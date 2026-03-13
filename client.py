import socket
def initialize(host,port):
    global client_object


    client_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_object.connect((host,port))

def response(data):

    if data:
        # if data.split(":")[0].strip()=="[RESPONSE 110]":
        #     data_2 = client_object.recv(1024).decode()
        #     if data_2.split(":")[0].strip()=="[RESPONSE 111]":
        #         return data_2.split(":")[1].strip()
        #     else:
        #         return data
        # elif data.split(":")[0].strip()=="[RESPONSE 220]":
        #     data_2 = client_object.recv(1024).decode()
        #     if data_2.split(":")[0].strip()=="[RESPONSE 222]":
        #         return data_2.split(":")[1].strip()
        #     else:
        #         return data
        if data.split(":")[0].strip()=="[RESPONSE 111]" or data.split(":")[0].strip()=="[RESPONSE 222]":
            return data.split(":")[1].strip()
        elif data.split(":")[0].strip()=="[RESPONSE 5111]":
            return "1"+data.split(":")[1].strip()
        elif data.split(":")[0].strip()=="[RESPONSE 5222]":
            return "0"+data.split(":")[1].strip()
        else:
            return data
    else:
        return "[ERROR]: Connection dropped by peer. PLEASE CONTACT SERVER ADMIN"
        

def start():
    client_object.send("[REQUEST 100]: START SERVER".encode())
    return client_object.recv(1024).decode()

def stop():
    client_object.send("[REQUEST 200]: STOP SERVER".encode())
    return client_object.recv(1024).decode()

def status():
    client_object.send("[REQUEST 500]: SERVER STATUS CHECK".encode())
    return client_object.recv(1024).decode()

    


