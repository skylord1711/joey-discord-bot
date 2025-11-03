# Joey's Discord Bot

A comprehensive Discord bot with moderation, music, utility, custom commands, and AI chat features!

## Features

### 🛡️ Moderation
- `!kick @user [reason]` - Kick a member
- `!ban @user [reason]` - Ban a member
- `!unban <user_id>` - Unban a user
- `!mute @user [minutes] [reason]` - Timeout a member
- `!unmute @user` - Remove timeout
- `!warn @user [reason]` - Warn a member
- `!warnings [@user]` - Check warnings
- `!clear [amount]` - Delete messages (max 100)

### 🎵 Music
- `!join` - Join your voice channel
- `!play <url>` - Play a song from YouTube
- `!pause` - Pause the current song
- `!resume` - Resume playback
- `!skip` - Skip current song
- `!stop` - Stop and clear queue
- `!leave` - Leave voice channel
- `!queue` - Show music queue
- `!volume <0-100>` - Change volume

### 🔧 Utility
- `!ping` - Check bot latency
- `!serverinfo` - Server information
- `!userinfo [@user]` - User information
- `!avatar [@user]` - Get user's avatar
- `!remind <minutes> <message>` - Set a reminder
- `!poll <question> <option1> <option2> ...` - Create a poll
- `!say <message>` - Make bot say something
- `!embed <title> <description>` - Create embed
- `!roll [dice]` - Roll dice (e.g., 2d6)

### 📝 Custom Commands
- `!addcmd <trigger> <response>` - Add custom command
- `!delcmd <trigger>` - Delete custom command
- `!listcmds` - List all custom commands

### 🤖 AI Chat
- `!ask <question>` - Ask the AI anything
- `!reset` - Reset conversation history
- Mention the bot to chat with AI

## Setup Instructions

### 1. Create Discord Bot
1. Go to https://discord.com/developers/applications
2. Click "New Application" and give it a name
3. Go to "Bot" section and click "Add Bot"
4. Enable these Privileged Gateway Intents:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
5. Copy the bot token

### 2. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Configure Environment Variables
1. Copy `.env.example` to `.env`
2. Add your Discord bot token
3. Add your OpenAI API key (for AI chat feature)

### 4. Invite Bot to Server
1. Go to OAuth2 > URL Generator
2. Select scopes: `bot`, `applications.commands`
3. Select permissions:
   - Administrator (or select specific permissions)
4. Copy the generated URL and open it in browser
5. Select your server and authorize

### 5. Run the Bot
\`\`\`bash
python scripts/bot.py
\`\`\`

## Deployment

For 24/7 hosting, deploy to:
- **Railway** (recommended): https://railway.app
- **Heroku**: https://heroku.com
- **Replit**: https://replit.com
- **VPS** (DigitalOcean, Linode, etc.)

## Notes

- Music feature requires FFmpeg installed on the system
- AI chat requires OpenAI API key (costs money per request)
- Bot needs proper permissions in Discord server
- Some commands require specific Discord permissions

## Support

For issues or questions, contact Joey or check the Discord.py documentation: https://discordpy.readthedocs.io/
\`\`\`

```py file="scripts/cogs/welcomer.py" isDeleted="true"
...deleted...
