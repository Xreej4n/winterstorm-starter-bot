# Minecraft Server Starter Bot

<br>

A lightweight Discord bot that can **start, stop, and monitor a Minecraft server running on your local machine**.

The bot communicates with a local control daemon that launches the server and can even manages the **playit.gg tunnel**, allowing friends to connect even if your network is behind NAT.

---

<br><br>

# ✨ Features

* Start the Minecraft server remotely from Discord
* Stop the server safely
* Check if the server is currently running
* Optionally, even start the **playit.gg tunnel** automatically when the server starts
* Can make the server run **in the background with no visible terminal**
* Designed for **local-hosted Minecraft servers**
* Simple architecture using Python sockets

---

<br><br>

# 🎮 Commands

| Command   | Description                     |
| --------- | ------------------------------- |
| `/startserver`  | Starts the Minecraft server     |
| `/stopserver`   | Stops the Minecraft server      |
| `/status` | Checks if the server is running |

---

<br><br>

# 🚀 Running the Project

> [!IMPORTANT]
> Make sure you match the PROJECT requirements [here](#-requirements)



### 1. Enable RCON on the Minecraft Server
Open your Minecraft server's ` server.properties ` file and look for/create the following lines:

``` 
enable-rcon=false
rcon.password=
rcon.port=25575
```
Change them to the following:
```
enable-rcon=true
rcon.password=<your_desired_passw>
rcon.port=<default/your_desired_port>
```
>[!TIP]
> You may keep the RCON port the default or change it to a suitable free port

### 2. Create the Discord Bot

Follow the guide on creating the Discord Bot [here](#-creating--inviting-the-discord-bot)

### 3. Create the .env file
Follow the guide on Environment Variables setup [here](#️-environment-variables)

### 4. Install the libraries
Run the following command in your daemon directory:
` pip install -r requirements.txt `

### 5. Start the Control Daemon (local machine)

Run the server controller on the same machine as the Minecraft server:

```
python daemon.py
```

This script CAN:

* launch the Minecraft server
* start the playit tunnel
* stop the Minecraft server
* check the Minecraft server status

<br>


<br>

---
<br><br>

# ⚙️ Environment Variables


1. Create a file named `.env` in the daemon directory with the following contents:

```
BOT_TOKEN="your_discord_bot_token"
GUILD_ID="your_discord_server_id"
IS_TUNNEL=true/false
SERVER_FILE="path_to_your_mc_server_file"
RCON_PASSW="your_rcon_password"
RCON_PORT=your_rcon_port
```

Example:

```
BOT_TOKEN="MzA2hshAAHA65AxAYSGk"
GUILD_ID="127835812687358712"
IS_TUNNEL=true
SERVER_FILE="paper.jar"
RCON_PASSW="Test@123"
RCON_PORT=25575
```

<br>

> [!NOTE]
> `BOT_TOKEN`: Specify the Discord BOT's token. In the **Bot** tab. Click **"Reset Token"** (or "Copy Token"). Paste the token here<br>
> <br>`GUILD_ID`: Specify your Discord server's ID
> <br>`IS_TUNNEL`: specify true/false. Set true if using tunneling service playit.gg <br>
> <br>`SERVER_FILE`: specify the Minecraft Server JAR file path 
> <br><br>`RCON_PASSW`: Specify the Password to the Minecraft Server's RCON console access. Must be same as the one in `server.properties`
> <br><br> `RCON_PORT`: Specify the Minecraft server's RCON port. Must be same as the one in `server.properties`

---

<br><br>

# 📦 Requirements

* Python **3.10+**
* Access to Minecraft Server `server.properties `
* playit.gg client (ONLY IF USING TUNELLING SERVICE)
* Permission to create new files
* Permision to create/access environment variables
* Libraries in  ` requirements.txt `


---

<br><br>


# 🤖 Creating & Inviting the Discord Bot

Follow these steps to create your Discord bot, configure permissions, and invite it to your server.

<br>

## 1. Create a Discord Application

1. Go to the **Discord Developer Portal**: https://discord.com/developers/applications

2. Click **"New Application"**

3. Enter a name (e.g., `Minecraft Control Bot`)

4. Click **Create**

<br>

## 2. Add a Bot to the Application

1. In the left sidebar, click **"Bot"**
2. Click **"Add Bot"**
3. Confirm by clicking **"Yes, do it!"**

<br>

## 3. Get the Bot Token

1. In the **Bot** tab
2. Click **"Reset Token"** (or "Copy Token")
3. Copy the token

>[!IMPORTANT]
> * Never share this token publicly
> * Treat it like a password

<br>

## 4. Enable Required Intents

Still in the **Bot** tab, scroll down to **Privileged Gateway Intents**.

Enable:

* Message Content Intent
* (Optional) Server Members Intent

<br>

## 5. Set Bot Permissions

Go to **OAuth2 → URL Generator**

### Select Scopes:

* `bot`
* `applications.commands`

### Select Bot Permissions:

Minimum required:

* Send Messages
* Use Slash Commands

Recommended:

* Read Message History
* Embed Links

<br>

## 6. Generate Invite Link

After selecting scopes and permissions:

1. Scroll down
2. Copy the generated URL

Example:

```id="3j1l9g"
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=274877906944&scope=bot%20applications.commands
```

<br>

## 7. Invite Bot to Your Server

1. Open the invite link in your browser
2. Select your server (guild)
3. Click **Authorize**
4. Complete the CAPTCHA

---



<br><br>

# 📜 License

MIT License

---
<br><br>

# ✒️ Author
A tool by Xreej4n. <br>
Created as a custom lightweight Minecraft server automation tool.

