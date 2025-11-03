import discord
from discord import app_commands
from discord.ext import commands
import os
from openai import AsyncOpenAI

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.conversation_history = {}

    @app_commands.command(name='ask', description='Ask the AI a question')
    @app_commands.describe(question='Your question for the AI')
    async def ask(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        
        try:
            user_id = interaction.user.id
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            self.conversation_history[user_id].append({
                "role": "user",
                "content": question
            })
            
            if len(self.conversation_history[user_id]) > 10:
                self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful Discord bot assistant named Joey's Bot. Be friendly and concise."},
                    *self.conversation_history[user_id]
                ],
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            self.conversation_history[user_id].append({
                "role": "assistant",
                "content": answer
            })
            
            if len(answer) > 2000:
                for i in range(0, len(answer), 2000):
                    await interaction.followup.send(answer[i:i+2000])
            else:
                await interaction.followup.send(answer)
                
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)}\nMake sure OPENAI_API_KEY is set!")

    @app_commands.command(name='reset', description='Reset your AI conversation history')
    async def reset(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
        await interaction.response.send_message("✅ Conversation history reset!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if self.bot.user in message.mentions:
            question = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
            if not question:
                return await message.channel.send("👋 Hi! Ask me anything using `/ask <question>`")

async def setup(bot):
    await bot.add_cog(AIChat(bot))
