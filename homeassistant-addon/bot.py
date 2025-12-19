import os
import discord
from discord import app_commands
from discord.ui import Button, View
from dotenv import load_dotenv
from typing import Dict, List, Set, Optional

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


class GameSession:
    """Represents a game session with players and game options."""
    
    def __init__(self, creator_id: int, channel_id: int):
        self.creator_id = creator_id
        self.channel_id = channel_id
        self.games: Dict[str, Dict] = {}  # game_name: {min_players, max_players, players: set}
        self.message_id: Optional[int] = None
        self.notified_games: Set[str] = set()  # Track which games have been notified
    
    def add_game(self, game_name: str, min_players: Optional[int], max_players: Optional[int]) -> bool:
        """Add a game to the session."""
        if game_name in self.games:
            return False
        self.games[game_name] = {
            'min_players': min_players,
            'max_players': max_players,
            'players': set()
        }
        return True
    
    def join_game(self, game_name: str, user_id: int) -> bool:
        """Add a player to a game."""
        if game_name not in self.games:
            return False
        
        game = self.games[game_name]
        if game['max_players'] is not None and len(game['players']) >= game['max_players']:
            return False
        
        game['players'].add(user_id)
        return True
    
    def leave_game(self, game_name: str, user_id: int) -> bool:
        """Remove a player from a game."""
        if game_name not in self.games:
            return False
        
        game = self.games[game_name]
        if user_id in game['players']:
            game['players'].remove(user_id)
            return True
        return False
    
    def get_ready_games(self) -> List[str]:
        """Get list of games that have reached minimum players."""
        ready = []
        for game_name, game in self.games.items():
            if game['min_players'] is not None and len(game['players']) >= game['min_players'] and game_name not in self.notified_games:
                ready.append(game_name)
        return ready
    
    def mark_notified(self, game_name: str):
        """Mark a game as having been notified."""
        self.notified_games.add(game_name)


# Store active sessions (channel_id: GameSession)
active_sessions: Dict[int, GameSession] = {}


class GameButton(Button):
    """Button for joining/leaving a game."""
    
    def __init__(self, game_name: str, session: GameSession):
        super().__init__(
            label=f"Join {game_name}",
            style=discord.ButtonStyle.primary,
            custom_id=f"join_{game_name}"
        )
        self.game_name = game_name
        self.session = session
    
    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        game = self.session.games.get(self.game_name)
        
        if not game:
            await interaction.response.send_message("This game no longer exists!", ephemeral=True)
            return
        
        # Toggle join/leave
        if user_id in game['players']:
            self.session.leave_game(self.game_name, user_id)
            await interaction.response.send_message(f"You left {self.game_name}!", ephemeral=True)
        else:
            if self.session.join_game(self.game_name, user_id):
                await interaction.response.send_message(f"You joined {self.game_name}!", ephemeral=True)
                
                # Check if minimum players reached
                if game['min_players'] is not None and len(game['players']) >= game['min_players'] and self.game_name not in self.session.notified_games:
                    self.session.mark_notified(self.game_name)
                    channel = client.get_channel(self.session.channel_id)
                    if channel:
                        player_mentions = ' '.join([f"<@{pid}>" for pid in game['players']])
                        await channel.send(
                            f"🎮 **{self.game_name}** has reached the minimum number of players! "
                            f"({len(game['players'])}/{game['min_players']})\n"
                            f"Players: {player_mentions}"
                        )
            else:
                await interaction.response.send_message(
                    f"Cannot join {self.game_name} - game is full!", 
                    ephemeral=True
                )
        
        # Update the message
        await update_session_message(interaction.message, self.session)


class AddGameButton(Button):
    """Button for adding a new game to the session."""
    
    def __init__(self):
        super().__init__(
            label="➕ Add Game",
            style=discord.ButtonStyle.success,
            custom_id="add_game"
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddGameModal())


class AddGameModal(discord.ui.Modal, title="Add a New Game"):
    """Modal for adding a new game."""
    
    game_name = discord.ui.TextInput(
        label="Game Name",
        placeholder="Enter the game name...",
        required=True,
        max_length=100
    )
    
    min_players = discord.ui.TextInput(
        label="Minimum Players (Optional)",
        placeholder="Leave blank for no minimum",
        required=False,
        max_length=3
    )
    
    max_players = discord.ui.TextInput(
        label="Maximum Players (Optional)",
        placeholder="Leave blank for no maximum",
        required=False,
        max_length=3
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        channel_id = interaction.channel_id
        session = active_sessions.get(channel_id)
        
        if not session:
            await interaction.response.send_message(
                "No active session in this channel! Use /lfg to start one.",
                ephemeral=True
            )
            return
        
        try:
            # Parse min and max players (None if empty)
            min_p = int(self.min_players.value) if self.min_players.value.strip() else None
            max_p = int(self.max_players.value) if self.max_players.value.strip() else None
            
            # Validate player counts
            if min_p is not None and min_p < 1:
                await interaction.response.send_message(
                    "Invalid minimum player count! Must be at least 1.",
                    ephemeral=True
                )
                return
            
            if max_p is not None and max_p < 1:
                await interaction.response.send_message(
                    "Invalid maximum player count! Must be at least 1.",
                    ephemeral=True
                )
                return
            
            if min_p is not None and max_p is not None and max_p < min_p:
                await interaction.response.send_message(
                    "Invalid player counts! Maximum must be >= minimum.",
                    ephemeral=True
                )
                return
            
            game_name = self.game_name.value
            if session.add_game(game_name, min_p, max_p):
                await interaction.response.send_message(
                    f"Added **{game_name}** to the session!",
                    ephemeral=True
                )
                
                # Update the session message
                if session.message_id:
                    channel = client.get_channel(channel_id)
                    if channel:
                        try:
                            message = await channel.fetch_message(session.message_id)
                            await update_session_message(message, session)
                        except discord.NotFound:
                            pass
            else:
                await interaction.response.send_message(
                    f"**{game_name}** is already in the session!",
                    ephemeral=True
                )
        except ValueError:
            await interaction.response.send_message(
                "Player counts must be valid numbers!",
                ephemeral=True
            )


def create_session_view(session: GameSession) -> View:
    """Create a view with buttons for all games in the session."""
    view = View(timeout=None)
    
    for game_name in session.games:
        view.add_item(GameButton(game_name, session))
    
    view.add_item(AddGameButton())
    
    return view


def create_session_embed(session: GameSession) -> discord.Embed:
    """Create an embed displaying the session information."""
    embed = discord.Embed(
        title="🎮 Looking for Group Session",
        description="Click the buttons below to join games or add new ones!",
        color=discord.Color.blue()
    )
    
    if not session.games:
        embed.add_field(
            name="No games yet",
            value="Click 'Add Game' to get started!",
            inline=False
        )
    else:
        for game_name, game in session.games.items():
            players_list = [f"<@{pid}>" for pid in game['players']]
            players_text = ', '.join(players_list) if players_list else "No players yet"
            
            # Build player count display
            if game['min_players'] is None and game['max_players'] is None:
                player_count = f"({len(game['players'])} players)"
                status = ""
            elif game['min_players'] is None:
                player_count = f"({len(game['players'])}/{game['max_players']})"
                status = ""
            elif game['max_players'] is None:
                player_count = f"({len(game['players'])}/{game['min_players']}+)"
                status = "✅ Ready!" if len(game['players']) >= game['min_players'] else "⏳ Waiting"
            else:
                player_count = f"({len(game['players'])}/{game['min_players']}-{game['max_players']})"
                status = "✅ Ready!" if len(game['players']) >= game['min_players'] else "⏳ Waiting"
            
            name = f"{game_name} {player_count} {status}".strip()
            
            embed.add_field(
                name=name,
                value=players_text,
                inline=False
            )
    
    return embed


async def update_session_message(message: discord.Message, session: GameSession):
    """Update the session message with current information."""
    embed = create_session_embed(session)
    view = create_session_view(session)
    await message.edit(embed=embed, view=view)


@tree.command(name="lfg", description="Start a looking-for-group session")
@app_commands.describe(
    game="Name of the first game (optional)",
    min_players="Minimum number of players (optional)",
    max_players="Maximum number of players (optional)"
)
async def lfg_command(
    interaction: discord.Interaction,
    game: str = None,
    min_players: int = None,
    max_players: int = None
):
    """Start a new LFG session."""
    channel_id = interaction.channel_id
    
    # Check if there's already an active session
    if channel_id in active_sessions:
        await interaction.response.send_message(
            "There's already an active LFG session in this channel!",
            ephemeral=True
        )
        return
    
    # Validate player counts
    if min_players is not None and min_players < 1:
        await interaction.response.send_message(
            "Invalid minimum player count! Must be at least 1.",
            ephemeral=True
        )
        return
    
    if max_players is not None and max_players < 1:
        await interaction.response.send_message(
            "Invalid maximum player count! Must be at least 1.",
            ephemeral=True
        )
        return
    
    if min_players is not None and max_players is not None and max_players < min_players:
        await interaction.response.send_message(
            "Invalid player counts! Maximum must be >= minimum.",
            ephemeral=True
        )
        return
    
    # Create new session
    session = GameSession(interaction.user.id, channel_id)
    
    # Add initial game if provided
    if game:
        session.add_game(game, min_players, max_players)
    
    active_sessions[channel_id] = session
    
    # Create and send the session message
    embed = create_session_embed(session)
    view = create_session_view(session)
    
    await interaction.response.send_message(embed=embed, view=view)
    
    # Store the message ID
    message = await interaction.original_response()
    session.message_id = message.id


@tree.command(name="endlfg", description="End the current looking-for-group session")
async def endlfg_command(interaction: discord.Interaction):
    """End the LFG session in the current channel."""
    channel_id = interaction.channel_id
    
    if channel_id not in active_sessions:
        await interaction.response.send_message(
            "There's no active LFG session in this channel!",
            ephemeral=True
        )
        return
    
    session = active_sessions[channel_id]
    
    # Only the creator or someone with manage messages permission can end the session
    if interaction.user.id != session.creator_id and not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "Only the session creator or users with 'Manage Messages' permission can end the session!",
            ephemeral=True
        )
        return
    
    # Delete the session message if it exists
    if session.message_id:
        try:
            channel = interaction.channel
            message = await channel.fetch_message(session.message_id)
            await message.delete()
        except discord.NotFound:
            pass  # Message was already deleted
        except discord.Forbidden:
            pass  # Bot doesn't have permission to delete
    
    # Remove the session
    del active_sessions[channel_id]
    
    await interaction.response.send_message("LFG session ended!", ephemeral=True)


@client.event
async def on_ready():
    """Called when the bot is ready."""
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print(f"Bot is ready! Logged in as {client.user}")
    print(f"Bot ID: {client.user.id}")


def main():
    """Main entry point."""
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: DISCORD_TOKEN not found in environment variables!")
        print("Please create a .env file with your bot token.")
        return
    
    client.run(token)


if __name__ == "__main__":
    main()
