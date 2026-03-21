# ❄️ Minecraft Server Control Bot

<br>

A lightweight Discord bot that can **start, stop, and monitor a Minecraft server running on your local machine**.

The bot communicates with a local control daemon that launches the server and manages the **playit.gg tunnel**, allowing friends to connect even if your network is behind NAT.

---

<br><br>

# ✨ Features

* Start the Minecraft server remotely from Discord
* Stop the server safely
* Check if the server is currently running
* Optionally, even start the **playit.gg tunnel** automatically when the server starts
* Server runs **in the background with no visible terminal**
* Designed for **local-hosted Minecraft servers**
* Simple architecture using Python sockets

---

<br><br>

# Commands

| Command   | Description                     |
| --------- | ------------------------------- |
| `/startserver`  | Starts the Minecraft server     |
| `/stopserver`   | Stops the Minecraft server      |
| `/status` | Checks if the server is running |

---

<br><br>

# 🚀 Running the Project

> [!NOTE]
> There are two parts to this program -- A local control daemon program and the Discord Bot program. Throughout the guide, we will be referring to them by the safe.

> [!IMPORTANT]
> Make sure you match the PROJECTrequirements [here](#-requirements)

```
Discord Bot
     │
     │ socket connection
     ▼
Local Control Daemon
     │
     ├── Starts Minecraft Server
     └── (OPTIONAL) Starts playit.gg Tunnel
```

The control daemon **must run on the same machine as the Minecraft server**. <br>
*Move the ` server.py ` to the Minecraft Server machine*

The Discord bot can run on **any machine, including the control daemon's machine** <br>
*All the rest of the files belong to the Discord Bot program*

<br><br>

## Local Control Daemon Program

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

### 2. Create the .env file
Follow the guide on Environment Variables setup [here](#local-control-daemon-1)

### 3. Install the libraries
Run the following command in your daemon directory:
` pip install -r requirements-server.txt `

### 4. Start the Control Daemon (local machine)

Run the server controller on the same machine as the Minecraft server:

```
python server.py
```

This script:

* listens for bot requests
* launches the Minecraft server
* starts the playit tunnel

<br>


<br>

## Discord BOT program 
### 1. Create the Discord Bot

Follow the guide on creating the Discord Bot [here](#-creating--inviting-the-discord-bot)

### 2. Create the .env file
Follow the guide on Environment Variables setup [here](#discord-bot-1)

### 3. Install the libraries
Run the following command in your bot directory:
` pip install -r requirements-client.txt `

### 4. Start the Discord Bot Program

Run the Discord Bot:

```
python client.py
```

This script:

* starts the discord bot
* accepts and process slash commands from Discord
* communicates with the local daemon

---
<br><br>

# ⚙️ Environment Variables

## Discord Bot
<small>Follow these steps for the discord bot program:</small> <br><br>
1. Create a file named `.env` in the bot directory with the following contents:

```
BOT_TOKEN="your_discord_bot_token"
GUILD_ID="your_discord_server_id"
HOST="your_local_control_daemon_ip"
PORT=your_local_control_daemon_port
```

Example:

```
BOT_TOKEN="MzA2hshAAHA65AxAYSGk"
GUILD_ID="127835812687358712"
HOST="127.0.0.1"
PORT=5000
```

<br><br>
`BOT_TOKEN`: Specify the Discord BOT's token. In the **Bot** tab. Click **"Reset Token"** (or "Copy Token"). Paste the token here<br>
<br>`GUILD_ID`: Specify your Minecraft server's ID
<br><br> `PORT`: Specify the port on which the bot should be communicating. Must be free and should be the same as the one set in the local daemon program
<br><br>`HOST`: Specify the local daemon's HOSTNAME, i.e. usually the local daemon's IP


---
## Local Control Daemon

<small>Follow these steps for the local control daemon program:</small> <br><br>
1. Create a file named `.env` in the daemon directory with the following contents:

```
IS_TUNNEL=true/false
SERVER_FILE="<path_to_minecraft_server_jar>"
PORT=<free_port_for_daemon>
RCON_PASSW="<your_rcon_password>"
RCON_PORT=<your_minecraft_rcon_port>
```

Example:

```
IS_TUNNEL=true
SERVER_FILE="paper.jar"
PORT=5000
RCON_PASSW="Test@123"
RCON_PORT=25575
```
<br><br>
`IS_TUNNEL`: specify true/false. Set true if using tunneling service playit.gg <br>
<br>`SERVER_FILE`: specify the Minecraft Server JAR file path 
<br><br> `PORT`: Specify the port on which the daemon should be listening. Must be free and should be the same as the one set in the discord bot program
<br><br>`RCON_PASSW`: Specify the Password to the Minecraft Server's RCON console access. Must be same as the one in `server.properties`
<br><br> `RCON_PORT`: Specify the Minecraft server's RCON port. Must be same as the one in `server.properties`


---

<br><br>

# 📦 Requirements

## Local Control Daemon
* Python **3.10+**
* Access to Minecraft Server `server.properties `
* playit.gg client (ONLY IF USING TUNELLING SERVICE)
* Libraries in  ` requirements-server.txt `

## Discord bot
* Python **3.10+**
* Libraries in  ` requirements-client.txt `

---

<br><br>


# 🤖 Creating & Inviting the Discord Bot

Follow these steps to create your Discord bot, configure permissions, and invite it to your server.

<br>

## 1. Create a Discord Application

1. Go to the **Discord Developer Portal**
   👉 https://discord.com/developers/applications

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

⚠️ **IMPORTANT:**

* Never share this token publicly
* Treat it like a password

<br>

## 4. Enable Required Intents

Still in the **Bot** tab, scroll down to **Privileged Gateway Intents**.

Enable:

* ✅ Message Content Intent
* (Optional) Server Members Intent

<br>

## 5. Set Bot Permissions

Go to **OAuth2 → URL Generator**

### Select Scopes:

* ✅ `bot`
* ✅ `applications.commands`

### Select Bot Permissions:

Minimum required:

* ✅ Send Messages
* ✅ Use Slash Commands

Recommended:

* ✅ Read Message History
* ✅ Embed Links

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



<br>

# License

MIT License

---
<br>

# Author
A tool by Xreej4n. <br>
Created as a custom lightweight Minecraft server automation tool.

