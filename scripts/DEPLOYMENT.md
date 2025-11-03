# Deploying Joey's Discord Bot to Fly.io

## Prerequisites

1. Install Fly.io CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Create a Fly.io account: `flyctl auth signup`
3. Have your Discord bot token and API keys ready

## Deployment Steps

### 1. Login to Fly.io
\`\`\`bash
flyctl auth login
\`\`\`

### 2. Navigate to the bot directory
\`\`\`bash
cd scripts
\`\`\`

### 3. Launch the app (first time only)
\`\`\`bash
flyctl launch
\`\`\`

When prompted:
- Choose an app name (or use the default)
- Select a region closest to you
- Don't add a PostgreSQL database
- Don't deploy yet (we need to set secrets first)

### 4. Set your environment variables as secrets
\`\`\`bash
flyctl secrets set DISCORD_TOKEN="your_discord_bot_token"
flyctl secrets set OPENAI_API_KEY="your_openai_api_key"
flyctl secrets set WELCOME_CHANNEL_ID="your_channel_id"
flyctl secrets set GOODBYE_CHANNEL_ID="your_channel_id"
\`\`\`

### 5. Deploy the bot
\`\`\`bash
flyctl deploy
\`\`\`

### 6. Check if it's running
\`\`\`bash
flyctl status
flyctl logs
\`\`\`

## Updating the Bot

After making code changes:

### From GitHub (Recommended)
1. Push changes to GitHub
2. Run: `flyctl deploy`

### From Local Machine
1. Navigate to scripts directory
2. Run: `flyctl deploy`

## Monitoring

- **View logs**: `flyctl logs`
- **Check status**: `flyctl status`
- **SSH into VM**: `flyctl ssh console`
- **Restart bot**: `flyctl apps restart joey-discord-bot`

## Troubleshooting

### Bot won't start
- Check logs: `flyctl logs`
- Verify secrets are set: `flyctl secrets list`
- Make sure Discord token is valid

### Out of memory
- Upgrade to larger VM: `flyctl scale memory 512`
- This will use paid tier ($1.94/month)

### Music not working
- Ensure ffmpeg is installed (included in Dockerfile)
- Check if yt-dlp is up to date
- Music uses significant bandwidth - monitor usage

## Free Tier Limits

- 3 shared-cpu VMs with 256MB RAM
- 160GB bandwidth/month
- If you exceed limits, you'll need to upgrade

## Stopping the Bot

\`\`\`bash
flyctl apps destroy joey-discord-bot
\`\`\`

## Support

- Fly.io Docs: https://fly.io/docs/
- Discord.py Docs: https://discordpy.readthedocs.io/
