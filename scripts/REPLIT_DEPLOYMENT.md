# Deploy Joey's Discord Bot on Replit (100% FREE)

No credit card required! This guide will help you deploy the bot on Replit's free tier.

## Step 1: Create Replit Account

1. Go to [replit.com](https://replit.com)
2. Sign up for free (no credit card needed)
3. Verify your email

## Step 2: Create New Repl

1. Click "Create Repl"
2. Select "Import from GitHub" OR "Python" template
3. Name it "joey-discord-bot"

## Step 3: Upload Bot Files

If you didn't import from GitHub:
1. Upload all files from the `scripts` folder
2. Make sure the folder structure looks like:
   \`\`\`
   joey-discord-bot/
   ├── bot_replit.py (rename this to bot.py)
   ├── keep_alive.py
   ├── cogs/
   │   ├── moderation.py
   │   ├── music.py
   │   ├── utility.py
   │   ├── custom_commands.py
   │   ├── welcomer.py
   │   └── ai_chat.py
   └── replit_requirements.txt (rename to requirements.txt)
   \`\`\`

## Step 4: Set Environment Variables (Secrets)

1. Click the lock icon on the left sidebar (Secrets)
2. Add these secrets:
   - `DISCORD_TOKEN`: Your Discord bot token
   - `OPENAI_API_KEY`: Your OpenAI API key (for AI chat)
   - `WELCOME_CHANNEL_ID`: Channel ID for welcome messages (optional)

## Step 5: Install Dependencies

Replit will auto-install from `requirements.txt`, but if not:
1. Open the Shell tab
2. Run: `pip install -r requirements.txt`

## Step 6: Run the Bot

1. Click the green "Run" button at the top
2. Your bot should come online!
3. Check the console for "Bot is now online!"

## Step 7: Keep Bot Running 24/7 (Important!)

Replit free tier puts inactive apps to sleep after 1 hour. To keep it awake:

### Option A: UptimeRobot (Recommended)
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Sign up for free
3. Create a new monitor:
   - Type: HTTP(s)
   - URL: Your Replit URL (shown when bot runs, looks like `https://joey-discord-bot.username.repl.co`)
   - Interval: Every 5 minutes
4. UptimeRobot will ping your bot every 5 minutes to keep it awake

### Option B: Replit Always On (Paid)
- Costs $7/month but keeps bot running without pings
- Only needed if you want guaranteed uptime

## Important Notes

**Music Feature Limitation:**
- Replit's free tier has limited bandwidth
- Music streaming might be slow or hit limits
- Consider disabling music cog if you don't need it:
  - Comment out `'music'` in the cogs list in bot.py

**Free Tier Limits:**
- 1GB RAM
- 1GB storage
- May sleep after inactivity (use UptimeRobot)
- Slower performance than paid hosting

**Getting Discord Bot Token:**
1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Create New Application
3. Go to "Bot" section
4. Click "Reset Token" and copy it
5. Enable these intents:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
6. Go to OAuth2 > URL Generator
7. Select scopes: `bot`, `applications.commands`
8. Select permissions: Administrator (or specific ones)
9. Copy the URL and invite bot to your server

## Troubleshooting

**Bot goes offline after 1 hour:**
- Set up UptimeRobot (see Step 7)

**Music not working:**
- Replit may block some audio streaming
- Try using smaller audio files
- Consider disabling music feature

**Bot is slow:**
- Free tier has limited resources
- Normal for free hosting

**Import errors:**
- Make sure all files are uploaded correctly
- Check that requirements.txt is installed

## Commands to Test

- `!help` - See all commands
- `!ping` - Check if bot is responsive
- `!serverinfo` - Test utility commands
- `!addcommand test Hello!` - Test custom commands

Enjoy your free Discord bot!
