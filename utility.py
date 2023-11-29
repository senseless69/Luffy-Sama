import nextcord
from nextcord.ext import commands
import sqlite3

class Utility(commands.Cog):
  def __init__(self, client):
    self.bot = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("Utility cog is ready.")
    db = sqlite3.connect("profanity.sqlite")
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS profanity(guild_id INTEGER, enable BOOLEAN)''')
    db.commit()
    cursor.close()
    db.close()

  @commands.command(pass_context = True)
  @commands.has_permissions(administrator= True)
  async def enable_profanity(self,ctx):
    db = sqlite3.connect("profanity.sqlite")
    cursor = db.cursor()
    cursor.execute('''SELECT enable FROM profanity WHERE guild_id = ?''', (ctx.guild.id,))
    result = cursor.fetchone()
    if result is None:
      cursor.execute('''INSERT INTO profanity VALUES(?, ?)''', (ctx.guild.id, False))
    try:
      bool = result[0]
    except:
      bool = result
    if bool == True:
      await ctx.send("Profanity is already enabled.")
    else:
      cursor.execute('''UPDATE profanity SET enable = ? WHERE guild_id = ?''', (True, ctx.guild.id))
      await ctx.send(f"Profanity has been enabled.")
      
    db.commit()
    cursor.close()
    db.close()

  @commands.command(pass_context = True)
  @commands.has_permissions(administrator = True)
  async def disable_profanity(self,ctx):
    db = sqlite3.connect("profanity.sqlite")
    cursor = db.cursor()
    cursor.execute('''SELECT enable FROM profanity WHERE guild_id = ?''', (ctx.guild.id,))
    result = cursor.fetchone()
    if result is None:
      cursor.execute('''INSERT INTO profanity VALUES(?, ?)''', (ctx.guild.id, True))
    try:
      bool = result[0]
    except:
      bool = result
    if bool == False:
      await ctx.send("Profanity is already disabled.")
    else:
      cursor.execute('''UPDATE profanity SET enable = ? WHERE guild_id = ?''', (False, ctx.guild.id))
      await ctx.send(f"Profanity has been disabled.")

    db.commit()
    cursor.close()
    db.close()

  @enable_profanity.error
  async def enable_profanity_error(self, ctx, error):
     if isinstance(error, commands.MissingPermissions):
       embed3 = nextcord.Embed(color = nextcord.Color.random(), title = "So Sad", description= "You don't have permission to run this command")
       await ctx.send(embed=embed3)
  @disable_profanity.error
  async def disable_profanity_error(self, ctx, error):
     if isinstance(error, commands.MissingPermissions):
       embed3 = nextcord.Embed(color = nextcord.Color.random(), title = "So Sad", description= "You don't have permission to run this command")
       await ctx.send(embed=embed3)

def setup(client):
  client.add_cog(Utility(client))
      

