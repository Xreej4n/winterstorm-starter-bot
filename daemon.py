import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
import socket
import subprocess
import threading
from mcrcon import MCRcon
from pathlib import Path
import sys
import platform
import time


if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

bot_token = str(os.environ['BOT_TOKEN'])
guild_id = str(os.environ['GUILD_ID'])


### ENV variables loading statements
is_tunnel = str(os.environ['IS_TUNNEL'])
server_file = str(os.environ['SERVER_FILE'])
rcon_passw = str(os.environ['RCON_PASSW'])
rcon_port=int(os.environ['RCON_PORT'])


############## START REDUNDANT CODE (to be removed in next release) ###################
# ###################### CLIENT CODE START ############################
# import socket
# def initialize(host,port):
#     global client_object


#     client_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_object.connect((host,port))

# def response(data):

#     if data:
#         if data.split(":")[0].strip()=="[RESPONSE 111]" or data.split(":")[0].strip()=="[RESPONSE 222]":
#             return data.split(":")[1].strip()
#         elif data.split(":")[0].strip()=="[RESPONSE 5111]":
#             return "1"+data.split(":")[1].strip()
#         elif data.split(":")[0].strip()=="[RESPONSE 5222]":
#             return "0"+data.split(":")[1].strip()
#         else:
#             return data
#     else:
#         return "[ERROR]: Connection dropped by peer. PLEASE CONTACT SERVER ADMIN"
        

# def start():
#     client_object.send("[REQUEST 100]: START SERVER".encode())
#     return client_object.recv(1024).decode()

# def stop():
#     client_object.send("[REQUEST 200]: STOP SERVER".encode())
#     return client_object.recv(1024).decode()

# def status():
#     client_object.send("[REQUEST 500]: SERVER STATUS CHECK".encode())
#     return client_object.recv(1024).decode()


########################### CLIENT CODE END ####################################
############## END REDUNDANT CODE #######################################################



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




############# START Discord functions (functions for Discord commands) ###############


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

## BOT startup checks
@bot.event
async def on_ready():
 
    guild = discord.Object(id=guild_id)

    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

## BOT ping check command (DISCORD command to check if the Bot is alive)
@bot.tree.command(name="ping", description="Command to check if the bot is online.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")



## SERVER Start function (DISCORD command to start the server)
@bot.tree.command(name="startserver", description="Command to start minecraft server")
async def startserver(interaction: discord.Interaction):
    try:

        user= interaction.user
        embed = discord.Embed(
            title="Server: Starting",
            description="Minecraft server is starting...",
            color=0xf1c40f
        )

        embed.add_field(name="Notification", value="You will be pinged when the server starts!")
        await interaction.response.send_message(embed=embed)

        return_response = start_server()
        
        if return_response.split(":")[0].strip()=="ERROR":
            embed = discord.Embed(
                    title="ERROR",
                    description=return_response.split(":")[1].strip(),
                    color=0xf22e27
            )
            
        else:
                embed = discord.Embed(
                    title="Server: ON",
                    description=return_response,
                    color=0x53f10f

                )
        await interaction.followup.send(f"{user.mention}",embed=embed)
    
    except Exception as e:
        embed = discord.Embed(
                    title="ERROR",
                    description=e+". Please contact bot admin",
                    color=0x53f10f

                )
        await interaction.followup.send(embed=embed)
    

## SERVER Stop command (DISCORD command to stop the server)
@bot.tree.command(name="stopserver", description="Command to stop minecraft server")
async def stopserver(interaction: discord.Interaction):
    try:
        

        user= interaction.user
        embed = discord.Embed(
            title="Server: Stopping",
            description="Minecraft server is stopping...",
            color=0xf1c40f
        )

        embed.add_field(name="Notification", value="You will be pinged when the server stops!")
        await interaction.response.send_message(embed=embed)

        return_response = stop_server()
        
        if return_response.split(":")[0].strip()=="ERROR":
            embed = discord.Embed(
                    title="ERROR",
                    description=return_response.split(":")[1].strip(),
                    color=0xf22e27
            )
            
        else:
                embed = discord.Embed(
                    title="Server: OFF",
                    description=return_response,
                    color=0xf22e27

                )
        await interaction.followup.send(content=f"{user.mention}",embed=embed)

    except Exception as e:
        embed = discord.Embed(
                    title="ERROR",
                    description=e+". Please contact server admin",
                    color=0x53f10f

                )
        await interaction.followup.send(embed=embed)



## Server STATUS check command (DISCORD command to check status of server)
@bot.tree.command(name="status", description="Command to check minecraft server status")
async def status(interaction: discord.Interaction):

    try:

        user= interaction.user
        return_response = check_status()
        
        if return_response.split(":")[0].strip()=="ERROR":
            embed = discord.Embed(
                    title="ERROR",
                    description=return_response.split(":")[1].strip(),
                    color=0xf22e27
            )
            
        elif return_response[0]=="1":
                embed = discord.Embed(
                    title="Server Status: ON",
                    description=return_response[1:],
                    color=0x53f10f

                )
        elif return_response[0]=="0":
                embed = discord.Embed(
                    title="Server Status: OFF",
                    description=return_response[1:],
                    color=0xf22e27

                )
        await interaction.response.send_message(f"{user.mention}",embed=embed)

    except Exception as e:
        embed = discord.Embed(
                    title="ERROR",
                    description=e+". Please contact server admin",
                    color=0x53f10f

                )
        await interaction.followup.send(embed=embed)

############## END Discord functions ######################

######## DISCORD BOT run command ###########
bot.run(bot_token)
