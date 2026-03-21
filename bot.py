import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import client
load_dotenv()

bot_token = str(os.environ['BOT_TOKEN'])
guild_id = str(os.environ['GUILD_ID'])
host = str(os.environ['HOST'])
port = int(os.environ['PORT'])

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

@bot.tree.command(name="startserver", description="Command to start Winterstorm")
async def startserver(interaction: discord.Interaction):
    try:
        client.initialize(host,port)

        user= interaction.user
        embed = discord.Embed(
            title="Server: Starting",
            description="Winterstorm SMP is starting...",
            color=0xf1c40f
        )

        embed.add_field(name="Notification", value="You will be pinged when the server starts!")
        await interaction.response.send_message(embed=embed)

        return_response = client.response(client.start())
        
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
                    description=e+". Please contact server admin",
                    color=0x53f10f

                )
        await interaction.followup.send(embed=embed)
    

@bot.tree.command(name="stopserver", description="Command to stop Winterstorm")
async def stopserver(interaction: discord.Interaction):
    try:
        client.initialize(host,port)

        user= interaction.user
        embed = discord.Embed(
            title="Server: Stopping",
            description="Winterstorm SMP is stopping...",
            color=0xf1c40f
        )

        embed.add_field(name="Notification", value="You will be pinged when the server stops!")
        await interaction.response.send_message(embed=embed)

        return_response = client.response(client.stop())
        
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


@bot.tree.command(name="status", description="Command to check Winterstorm server status")
async def status(interaction: discord.Interaction):

    try:
        client.initialize(host,port)
        user= interaction.user
        return_response = client.response(client.status())
        
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
