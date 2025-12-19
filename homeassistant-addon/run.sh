#!/bin/sh
set -e

echo "[INFO] LFG Discord Bot starting..."

CONFIG_PATH=/data/options.json

if [ ! -f "$CONFIG_PATH" ]; then
    echo "[ERROR] Configuration file not found at $CONFIG_PATH"
    exit 1
fi

echo "[INFO] Reading configuration..."

# Get Discord token from add-on configuration
DISCORD_TOKEN=$(jq --raw-output '.discord_token // empty' $CONFIG_PATH)

if [ -z "$DISCORD_TOKEN" ]; then
    echo "[ERROR] Discord token not configured in add-on settings!"
    exit 1
fi

echo "[INFO] Token loaded successfully"

# Export token as environment variable
export DISCORD_TOKEN

echo "[INFO] Starting bot process..."

# Run the bot
cd /app
exec python3 -u bot.py
