# LFG Discord Bot

A Discord bot that helps users organize gaming sessions by expressing interest in games and tracking player counts.

## Features

- 🎮 Create gaming sessions with multiple games
- 👥 Set minimum and maximum player counts for each game
- ➕ Users can join games with a single button click
- 📢 Automatic notifications when minimum player count is reached
- ✨ Easy-to-use interface with interactive buttons
- ➕ Add new games to existing sessions on the fly

## How It Works

1. A user starts an LFG (Looking For Group) session using the `/lfg` command
2. They can optionally specify an initial game with min/max player counts
3. An interactive message appears with buttons for each game
4. Other users can click "Join" to express interest in any game
5. Users can also add new games to the session using the "Add Game" button
6. The bot tracks player counts and announces when a game reaches its minimum
7. Players can see who's interested in each game in real-time

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
6. Enable these Privileged Gateway Intents:
   - Message Content Intent
7. Go to "OAuth2" > "URL Generator"
8. Select scopes: `bot` and `applications.commands`
9. Select bot permissions: `Send Messages`, `Embed Links`, `Use Slash Commands`
10. Copy the generated URL and open it to invite your bot to your server

### Installation

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
```bash
cp .env.example .env
```

5. Edit `.env` and add your Discord bot token:
```
DISCORD_TOKEN=your_bot_token_here
```

### Running the Bot

```bash
python bot.py
```

You should see a message indicating the bot is ready!

## Usage

### Commands

#### `/lfg [game] [min_players] [max_players]`
Start a new LFG session in the current channel.

**Parameters:**
- `game` (optional): Name of the first game
- `min_players` (optional, default: 2): Minimum number of players
- `max_players` (optional, default: 4): Maximum number of players

**Examples:**
```
/lfg
/lfg game:"Valorant" min_players:5 max_players:5
/lfg game:"Among Us" min_players:4 max_players:10
```

#### `/endlfg`
End the current LFG session in the channel. Only the session creator or users with "Manage Messages" permission can end a session.

### Interacting with Sessions

Once a session is created:
- **Click "Join [Game]"** to join a game (click again to leave)
- **Click "➕ Add Game"** to add a new game to the session
- The message updates in real-time showing:
  - Current player count for each game
  - Min/max player requirements
  - List of players interested in each game
  - Status (✅ Ready when minimum is reached, ⏳ Waiting otherwise)

### Example Workflow

1. User A: `/lfg game:"Overwatch" min_players:6 max_players:6`
2. Bot creates an interactive message with an "Join Overwatch" button
3. Users B, C, D click "Join Overwatch"
4. User E clicks "➕ Add Game" and adds "League of Legends" (min: 5, max: 5)
5. Bot adds a new "Join League of Legends" button to the message
6. More users join games
7. When 6 people join Overwatch, bot announces: "🎮 Overwatch has reached the minimum number of players!"

## Technical Details

- Built with `discord.py` 2.3.2+
- Uses Discord's slash commands for easy interaction
- Utilizes Discord UI components (Buttons, Modals) for rich interactions
- Session data is stored in memory (resets when bot restarts)
- Each channel can have one active session at a time

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.