import socket
import subprocess
import threading
from mcrcon import MCRcon

HOST = "0.0.0.0"
PORT =5000

server = False
pid = False

def server_running():
    s2 = socket.socket()
    try:
        s2.connect(("127.0.0.1",25565))
        return True
    except:
        return False
    finally:
        s2.close()

def start_server():
    # global server_process

    # if server_process and server_process.poll() is None:
    #     return "[RESPONSE 111]: Server is already running"

    # try:
    #     server_process = subprocess.Popen(
    #         ["start.bat"],
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.STDOUT,
    #         stdin=subprocess.PIPE,
    #         text=True,
    #         shell=True
    #     )
    if server_running() is False:
        try :
            
        #         global server
        #         global pid
        #         server_dir = r"C:\Minecraft (server)"
        #         server = subprocess.Popen(
        #     f'start "MC Server" /D "{server_dir}" cmd /k java -Xms2G -Xmx2G -jar paper.jar nogui',
        #     shell=True
        # )
        #         pid = server.pid
        
            global mc_process, playit_process

            # start playit tunnel
            playit_process = subprocess.Popen(
                ["playit.exe"],
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # start minecraft server
            mc_process = subprocess.Popen(
                ["java","-Xms2G","-Xmx2G","-jar","paper.jar","nogui"],
                cwd=r"C:\Minecraft (server)",
                creationflags=subprocess.CREATE_NO_WINDOW
        )

            print("Server started")
            
            while server_running() is False:
                continue
            return "[RESPONSE 111]: Server is now running"

        except Exception as e:
            return f"Error starting server: {e}"
    else:
        return "[RESPONSE 111]: Server was already running"

def stop_server():
    # global server_process

    # if server_process.poll() is not None or server_process is None:
    #     return "[RESPONSE 222]: Server is already off"

    # try:
    #     server_process.stdin.write("stop\n")
    #     server_process.stdin.flush()
    #     return "[REPONSE 222]: Server has been stopped"

    # except Exception as e:
    #     return f"Error stopping server: {e}"
    
    
    # if server is False or pid is False:
    #     return "[RESPONSE 222]: Server is already off"
    # else:
    #     try:
    #         server.terminate()
    #         return "[REPONSE 222]: Server has been stopped"

    #     except Exception as e:
    #         return f"Error stopping server: {e}"
    
    try:
        if server_running():
            with MCRcon("127.0.0.1", "Mminecraftbroslimited123xreej4n", port=25575) as mcr:
                mcr.command("stop")
            server.terminate()
            playit_process.terminate()
            return "[REPONSE 222]: Server has been stopped"
        else:
            return "[RESPONSE 222]: Server is already off"
    except Exception as e:
        return f"Error stopping server: {e}"
    
    


def check_status():

    if server_running():
        return "[RESPONSE 5111]: Server is starting/already running"
    else:
        return "[RESPONSE 5222]: Server offline"



def handle_client(conn):

    data = conn.recv(1024).decode().strip()

    if data == "[REQUEST 100]: START SERVER":
        response = start_server()
        conn.send(response.encode())


    elif data == "[REQUEST 500]: SERVER STATUS CHECK":
        response = check_status()
        conn.send(response.encode())

    elif data=="[REQUEST 200]: STOP SERVER":
        response = stop_server()
        conn.send(response.encode())

    conn.close()


def main():

    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen()

    print("Server daemon running")

    while True:
        conn, addr = s.accept()

        threading.Thread(
            target=handle_client,
            args=(conn,),
            daemon=True
        ).start()


if __name__ == "__main__":
    main()