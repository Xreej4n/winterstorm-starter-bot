## Server side control script. Move this file to the Minecraft Server machine. 
## DO NOT MODIFY ANY CODE. PLEASE USE THE server.env file for config.
## Developed by Xreej4n


### Library Import statements
import socket
import subprocess
import threading
from mcrcon import MCRcon
from dotenv import load_dotenv
import os
from pathlib import Path
import sys
import platform
import time

### CWD accquire statements
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

### ENV variables loading statements
load_dotenv("server.py")

is_tunnel = str(os.environ['IS_TUNNEL'])
server_file = str(os.environ['SERVER_FILE'])
rcon_passw = str(os.environ['RCON_PASSW'])
port = int(os.environ['PORT'])
rcon_port=int(os.environ['RCON_PORT'])
HOST = "0.0.0.0"
PORT=port



############# START server control functions (functions for controlling the server) ###############

## SERVER run check function (provides code for pinging and checking if server running)
def server_running():
    try:
        with MCRcon("127.0.0.1", rcon_passw, port=rcon_port, timeout=5) as mcr:
            response = mcr.command("list") 
            return True
    except Exception:
        return False

## Server START function (provides code for starting the server)
def start_server():

    if server_running() is False:
        try :
        
        ############## START REDUNDANT CODE (to be removed in next release) ###################

        #     global mc_process, playit_process

        #     if is_tunnel.lower()=="true":
        #         playit_process = subprocess.Popen(
        #             ["playit.exe"],
        #             creationflags=subprocess.CREATE_NO_WINDOW
        #         )

        #     # start minecraft server
        #     mc_process = subprocess.Popen(
        #         ["java","-Xms2G","-Xmx2G","-jar",server_file,"nogui"],
        #         cwd=BASE_DIR,
        #         creationflags=subprocess.CREATE_NO_WINDOW
        # )

        ############## END REDUNDANT CODE #######################################################

            global mc_process, playit_process

            cmd = ["java", "-jar", "paper.jar", "nogui"]

            if platform.system() == "Windows":
                mc_process = subprocess.Popen(
                    cmd,
                    cwd=BASE_DIR,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                if is_tunnel.lower() =="true":
                    playit_process = subprocess.Popen(
                        ["playit"],
                        creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                mc_process = subprocess.Popen(
                    cmd,
                    cwd=BASE_DIR,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True
                )

                if is_tunnel.lower() == "true":
                        playit_process = subprocess.Popen(
                            ["playit"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            stdin=subprocess.DEVNULL,
                            start_new_session=True
                )

            print("Server started")
            
            while server_running() is False:
                continue
            return "[RESPONSE 111]: Server is now running"

        except Exception as e:
            return f"Error starting server: {e}"
    else:
        return "[RESPONSE 111]: Server was already running"
    
    
## Server STATUS check function (provides code for checking the status of server)
def check_status():

    if server_running():
        return "[RESPONSE 5111]: Server is starting/already running"
    else:
        return "[RESPONSE 5222]: Server offline"

## Server STOP command (provides code for stopping the server)
def stop_server():

    try:
        if server_running():
            with MCRcon("127.0.0.1", "rcon_passw", port=rcon_port) as mcr:
                mcr.command("stop")
            mc_process.terminate()
            playit_process.terminate()
            return "[REPONSE 222]: Server has been stopped"
        else:
            return "[RESPONSE 222]: Server is already off"
    except Exception as e:
        return f"Error stopping server: {e}"
    
########## END server control functions ###############



### CLIENT HANDLER (interprets messages sent by client)
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



#### MAIN FUNCTION (accepts and reads client requests)
def main():

    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()

        threading.Thread(
            target=handle_client,
            args=(conn,),
            daemon=True
        ).start()
        print("Server daemon running")
        time.sleep(2)


if __name__ == "__main__":
    main()