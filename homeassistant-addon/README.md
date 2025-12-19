# LFG Discord Bot - Home Assistant Add-on

This add-on runs the LFG Discord Bot as a Home Assistant add-on.

## Installation

1. Copy the `homeassistant-addon` folder to `/addons/lfg_discord_bot/` on your Home Assistant installation
2. Go to **Settings** → **Add-ons** → **Add-on Store**
3. Click the menu (⋮) in the top right → **Check for updates**
4. The "LFG Discord Bot" should appear in the local add-ons
5. Click on it and install

## Configuration

Add your Discord bot token in the add-on configuration:

```yaml
discord_token: "YOUR_DISCORD_BOT_TOKEN_HERE"
```

## Usage

After installation and configuration:
1. Start the add-on
2. Check the logs to verify it's running
3. The bot will be online in your Discord server

The add-on will automatically start with Home Assistant if "Start on boot" is enabled.
