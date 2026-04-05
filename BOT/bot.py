import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv("client.py")

bot_token = str(os.environ['BOT_TOKEN'])
guild_id = str(os.environ['GUILD_ID'])
host = str(os.environ['HOST'])
port = int(os.environ['PORT'])

###################### CLIENT CODE START ############################
import socket
def initialize(host,port):
    global client_object


    client_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_object.connect((host,port))

def response(data):

    if data:
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


########################### CLIENT CODE END ####################################

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
 
    guild = discord.Object(id=guild_id)

    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.tree.command(name="ping", description="Command to check if the bot is online.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="startserver", description="Command to start minecraft server")
async def startserver(interaction: discord.Interaction):
    try:
        initialize(host,port)

        user= interaction.user
        embed = discord.Embed(
            title="Server: Starting",
            description="Minecraft server is starting...",
            color=0xf1c40f
        )

        embed.add_field(name="Notification", value="You will be pinged when the server starts!")
        await interaction.response.send_message(embed=embed)

        return_response = response(start())
        
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
    

@bot.tree.command(name="stopserver", description="Command to stop minecraft server")
async def stopserver(interaction: discord.Interaction):
    try:
        initialize(host,port)

        user= interaction.user
        embed = discord.Embed(
            title="Server: Stopping",
            description="Minecraft server is stopping...",
            color=0xf1c40f
        )

        embed.add_field(name="Notification", value="You will be pinged when the server stops!")
        await interaction.response.send_message(embed=embed)

        return_response = response(stop())
        
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


@bot.tree.command(name="status", description="Command to check minecraft server status")
async def status(interaction: discord.Interaction):

    try:
        initialize(host,port)
        user= interaction.user
        return_response = response(status())
        
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


bot.run(bot_token)
