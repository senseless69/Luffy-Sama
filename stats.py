import aiohttp 
import nextcord , os
from nextcord.ext import commands , tasks
from bhbotlist import bhbotlist
import aiohttp # Use `pip install aiohttp` to install
import topgg
from botlistpy.helpers import SyncBotClient
dbl_token = "TOKEN"
class StatsUpload(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.VoidUpload.start()
    self.update_stats.start()
    self.bot.topggpy = topgg.DBLClient(self.bot, dbl_token)
    self.client = SyncBotClient(CLIENT_ID, "TOKEN")
    

  def cog_unload(self):
    self.VoidUpload.cancel()
  

  @tasks.loop(minutes = 30)
  async def VoidUpload(self):
    await self.bot.wait_until_ready()
    async with aiohttp.ClientSession() as session:
      async with session.post(url = f"https://api.voidbots.net/bot/stats/{self.bot.user.id}",
      headers = {
        "content-type":"application/json",
        "Authorization": "TOKEN"
        },
      json = {
        "server_count": len(self.bot.guilds),
        #"shard_count": len(self.bot.shards) #Uncomment this line if shards are used.
        }) as r:
        json = await r.json()
        print(json)
        

  @tasks.loop(minutes=30)
  async def update_stats(self):
      try:
          await self.bot.wait_until_ready()
          await self.bot.topggpy.post_guild_count()
          self.client.setStats(len(self.bot.guilds))
          print(f"Posted server count ({self.bot.topggpy.guild_count})")
      except Exception as e:
          print(f"Failed to post server count\n{e.__class__.__name__}: {e}")
        
def setup(bot):
 bot.add_cog(StatsUpload(bot))