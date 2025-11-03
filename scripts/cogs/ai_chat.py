import discord
from discord.ext import commands
import os
from openai import AsyncOpenAI

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.conversation_history = {}

    @commands.command(name='ask')
    async def ask(self, ctx, *, question):
        """Ask the AI a question"""
        async with ctx.typing():
            try:
                # Get or create conversation history for this user
                user_id = ctx.author.id
                if user_id not in self.conversation_history:
                    self.conversation_history[user_id] = []
                
                # Add user message to history
                self.conversation_history[user_id].append({
                    "role": "user",
                    "content": question
                })
                
                # Keep only last 10 messages to avoid token limits
                if len(self.conversation_history[user_id]) > 10:
                    self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
                
                # Get AI response
                response = await self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful Discord bot assistant named Joey's Bot. Be friendly and concise."},
                        *self.conversation_history[user_id]
                    ],
                    max_tokens=500
                )
                
                answer = response.choices[0].message.content
                
                # Add AI response to history
                self.conversation_history[user_id].append({
                    "role": "assistant",
                    "content": answer
                })
                
                # Send response
                if len(answer) > 2000:
                    # Split long messages
                    for i in range(0, len(answer), 2000):
                        await ctx.send(answer[i:i+2000])
                else:
                    await ctx.send(answer)
                    
            except Exception as e:
                await ctx.send(f"❌ Error: {str(e)}\nMake sure OPENAI_API_KEY is set!")

    @commands.command(name='reset')
    async def reset(self, ctx):
        """Reset your conversation history with the AI"""
        user_id = ctx.author.id
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
        await ctx.send("✅ Conversation history reset!")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Respond when bot is mentioned"""
        if message.author.bot:
            return
        
        # Check if bot is mentioned
        if self.bot.user in message.mentions:
            # Remove the mention from the message
            question = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
            if not question:
                return await message.channel.send("👋 Hi! Ask me anything using `!ask <question>`")
            
            # Create a fake context to use the ask command
            ctx = await self.bot.get_context(message)
            await self.ask(ctx, question=question)

async def setup(bot):
    await bot.add_cog(AIChat(bot))
