# LFG Discord Bot

A Discord bot that helps users organize gaming sessions by expressing interest in games and tracking player counts.

## Features

- 🎮 Create gaming sessions with multiple games
- 👥 Optional minimum and maximum player counts for each game
- ➕ Users can join games with a single button click
- 📢 Automatic notifications when minimum player count is reached
- ✨ Easy-to-use interface with interactive buttons
- ➕ Add new games to existing sessions on the fly
- 🏠 Can be deployed as a Home Assistant add-on
- 🔄 Session messages are automatically deleted when ending sessions

## How It Works

1. A user starts an LFG (Looking For Group) session using the `/lfg` command
2. They can optionally specify an initial game with min/max player counts
3. An interactive message appears with buttons for each game
4. Other users can click "Join" to express interest in any game
5. Users can also add new games to the session using the "Add Game" button
6. The bot tracks player counts and announces when a game reaches its minimum
7. Players can see who's interested in each game in real-time
8. When ending a session, the status message is automatically deleted

## Setup

### Prerequisites

- Python 3.8 or higher
- A Discord Bot Token (see below)

### Getting a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under "TOKEN", click "Reset Token" and copy your bot token
6. Go to "OAuth2" > "URL Generator"
7. Select scopes: `bot` and `applications.commands`
8. Select bot permissions: `Send Messages`, `Embed Links`, `Read Message History`, `Manage Messages`
9. Copy the generated URL and open it to invite your bot to your server

### Installation

#### Option 1: Standalone

1. Clone this repository:
```bash
git clone https://github.com/Slammus/LFGDiscordBot.git
cd LFGDiscordBot
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```
DISCORD_TOKEN=your_bot_token_here
```

5. Run the bot:
```bash
python bot.py
```

#### Option 2: Home Assistant Add-on

1. Copy the `homeassistant-addon` folder to `/addons/lfg_discord_bot/` on your Home Assistant installation
2. Go to **Settings** → **Add-ons** → **Add-on Store**
3. Click the menu (⋮) → **Check for updates**
4. Find "LFG Discord Bot" in Local add-ons
5. Click **Install**
6. In the **Configuration** tab, add your Discord token
7. Click **Start**
8. Enable **Start on boot** for automatic startup

See `homeassistant-addon/README.md` for more details.

## Usage

### Commands

#### `/lfg [game] [min_players] [max_players]`
Start a new LFG session in the current channel.

**Parameters:**
- `game` (optional): Name of the first game
- `min_players` (optional): Minimum number of players (leave blank for no minimum)
- `max_players` (optional): Maximum number of players (leave blank for no maximum)

**Examples:**
```
/lfg
/lfg game:"Valorant" min_players:5 max_players:5
/lfg game:"Among Us" min_players:4 max_players:10
/lfg game:"Minecraft"  # No player limits
```

#### `/endlfg`
End the current LFG session in the channel and delete the session message. Only the session creator or users with "Manage Messages" permission can end a session.

### Interacting with Sessions

Once a session is created:
- **Click "Join [Game]"** to join a game (click again to leave)
- **Click "➕ Add Game"** to add a new game to the session (min/max are optional)
- The message updates in real-time showing:
  - Current player count for each game
  - Min/max player requirements (or flexible player count if not set)
  - List of players interested in each game
  - Status (✅ Ready when minimum is reached, ⏳ Waiting otherwise, or no status if no minimum set)

### Example Workflow

1. User A: `/lfg game:"Overwatch" min_players:6 max_players:6`
2. Bot creates an interactive message with a "Join Overwatch" button
3. Users B, C, D click "Join Overwatch"
4. User E clicks "➕ Add Game" and adds "Minecraft" (no min/max specified)
5. Bot adds a new "Join Minecraft" button to the message showing flexible player count
6. More users join games
7. When 6 people join Overwatch, bot announces: "🎮 Overwatch has reached the minimum number of players!" and mentions all players
8. User A uses `/endlfg` to clean up the session message

## Technical Details

- Built with `discord.py` 2.6.4+
- Uses Discord's slash commands for easy interaction
- Utilizes Discord UI components (Buttons, Modals) for rich interactions
- Session data is stored in memory (resets when bot restarts)
- Each channel can have one active session at a time
- Supports deployment as a Home Assistant add-on for 24/7 availability

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.