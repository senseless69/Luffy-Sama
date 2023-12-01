import nextcord
import numpy
from nextcord.ext import commands, tasks
import sys
import traceback
import asyncpg
import disrank
from nextcord.ext.commands import when_mentioned_or
import json
import os
from nextcord.ext.commands import when_mentioned_or
import time
import asyncio
from better_profanity import profanity
import os
import datetime
import json
import sqlite3
import math
import sqlite3
from nextcord import *
import re
import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
import requests
import asyncio
import urllib
import aiohttp
import urllib.request
from requests import get
from itertools import cycle
import os
import aiosqlite
from keep_alive import keep_alive
keep_alive()


intents = nextcord.Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True
intents.guilds = True






  
client = commands.Bot(command_prefix=when_mentioned_or(''),
                    intents=intents)
client.remove_command('help')



@client.slash_command(name="help",description="Shows the help menu")
async def help(interaction: nextcord.Interaction):
  embed = nextcord.Embed(title="**Help**", description="Prefix : @—͟͞͞ Luffy Sama#5630\nChoose a  >category< for the extended version", color=nextcord.Color.random())
  embed.add_field(name="**Moderation**", value=" kick , ban , unban , clear , members")
  embed.add_field(name="**Fun**", value=" /meme, wanted ")
  embed.add_field(name= "**Utility**", value= " ping, enable_profanity(new), disable_profanity(new) ")
  embed.add_field(name="**Economy**", value="start , vote(new) , delete , bal , deposit , withdraw ,  beg , dice , coinflip , slots , open , sell , send , inventory , rob , shop , buy , fish ")
  await interaction.response.send_message(embed=embed, view = dropdown(client, interaction.user.id))


@client.command(name="ping",description="Shows the bots latency")
async def ping(ctx):
  time_1 = time.perf_counter()
  await ctx.trigger_typing()
  time_2 = time.perf_counter()
  ping = round((time_2-time_1)*1000)
  await ctx.send(f"**Pong!** in **`{ping}ms`**")

class helpdropdown(nextcord.ui.Select):
  def __init__(self, bot: commands.Bot, user):
    self.bot = bot
    self.user = user
    options = [
      nextcord.SelectOption(label="Moderation", description="Commands for moderation"),
      nextcord.SelectOption(label="Fun", description="Commands for fun"),
      nextcord.SelectOption(label="Utility",description="Commands for utility"),
      
      nextcord.SelectOption(label="Economy", description="Commands for Economy")]
    super().__init__(placeholder="Select a category", min_values=1, max_values=1, options=options)

  async def callback(self ,interaction: nextcord.Interaction):
    if int(interaction.user.id) != self.user:
      return await interaction.response.send_message("This is not for you", ephemeral=True)
    else:  
      if self.values[0] == "Moderation":
        embed = nextcord.Embed(title="**Moderation**", description="Moderation commands", color=nextcord.Color.random())
        embed.add_field(name="**kick**", value="Kicks a member")
        embed.add_field(name="**ban**", value="Bans a member")
        embed.add_field(name="**clear**", value="Clears a certain amount of messages")
        embed.add_field(name="**members**", value="Shows the amount of members in the server")
        await interaction.response.send_message(embed=embed)
      elif self.values[0] == "Fun":
        embed = nextcord.Embed(title="**Fun**", description="Fun commands", color=nextcord.Color.random())
        embed.add_field(name="**/meme**", value="Sends a random meme from reddit")
        embed.add_field(name="**wanted**", value="Sends a wanted poster of a user")
        
        await interaction.response.send_message(embed=embed) 
      elif self.values[0] == "Utility":
        embed = nextcord.Embed(title="**Utility**", description="Utility commands", color=nextcord.Color.random())
        embed.add_field(name="**ping**", value="Shows the bots latency")
        embed.add_field(name="**enable_profanity**", value="Enables profanity filter")
        embed.add_field(name="**disable_profanity**", value="Disables profanity filter")
        await interaction.response.send_message(embed=embed)
      

      else:
        embed = nextcord.Embed(title="**Economy**", description="Economy commands", color=nextcord.Color.random())
        embed.add_field(name="**start**", value="Starts a new account with a mandatory amount of 100$")
        embed.add_field(name="**vote**", value="Vote for the bot to get rewards")
        embed.add_field(name="**delete**", value="Deletes your account")
        embed.add_field(name="**bal**", value="Shows your balance")
        embed.add_field(name="**deposit**",value="Deposits money into your bank")
        embed.add_field(name="**withdraw**", value="Withdraws money from your bank")
        embed.add_field(name="**beg**", value="Begs for money")
        embed.add_field(name="**dice**", value="Rolls a dice and if you roll a number greater than bot you win double the bet money")
        embed.add_field(name="**coinflip**", value="Flips a coin and if you get the side chosen by you, you win double the bet money")
        embed.add_field(name="**slots**", value="Spins a slot machine and if you get all three slots chosen by you, you can win upto five times the bet money")
        embed.add_field(name="**open**", value="Opens a lootboxbox from which you can win a Pistol which is Ultra Rare(0.2%) and other items")
        embed.add_field(name="**inventory**", value="Shows your inventory")
        embed.add_field(name="**rob**", value="Robs a user and if you succeed you  win the amount of  money you want")
        embed.add_field(name="**sell**", value="Sells your items")
        embed.add_field(name="**send**", value="Sends money to a user")
        embed.add_field(name="**shop**", value="Shows the shop")
        embed.add_field(name="**buy**", value="Buys an item from the shop")
        embed.add_field(name="**fish**", value="Fishes for fish and if you get a fish you can sell it for money")
        await interaction.response.send_message(embed=embed)
        
      


class dropdown(nextcord.ui.View):
  def __init__(self, bot: commands.Bot, user):
    self.bot = bot
    self.user = user
    super().__init__()
    self.add_item(helpdropdown(bot = self.bot, user= self.user))


my_secret = os.environ['BOTTOKEN']
status = cycle(["#For Weebs", "/help | v1.2.0", "for {n} servers |{c} members"])
extensions = ["example.py", "moderation.py", "fun.py"]


@tasks.loop(seconds=10)
async def status_swap():
  name = next(status)
  name = name.format(n=len(client.guilds),c=f'{(len(client.users)):,}')
  await client.change_presence(activity=nextcord.Streaming(
      name=f"{name}",
      url=
      "https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUXbmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXA%3D"
  ))





@client.slash_command(name="hello",description="say hello to the bot")
async def hello(ctx):
  member = await client.fetch_user(820952511589646356)
  await ctx.send(embed=nextcord.Embed(title=f"Hello Weeb!", description=f"I am LuffySama, a multipurpose bot created by {member.mention}.My Prefix is  @—͟͞͞ Luffy Sama#5630 yes you have to ping me in order to call me and for more information On me and my Commands type /help and I will be there for your help.BTW if you don't know I am a moderation bot with some cool fun commands like  meme.I even have  economy commands like coinflip , dice, shop , inventory and many more.....", color = nextcord.Color.random()))

@client.event
async def on_ready():
  print("The bot is now ready for use!")
  print("-----------------------------")
  print(f"Currently in {len(client.guilds)} for {(len(client.users)):,} users ")
  status_swap.start()
  check.start()
 
  
  db2 = sqlite3.connect("vote.sqlite")
  cursor2 = db2.cursor()
  cursor2.execute('''CREATE TABLE IF NOT EXISTS vote(user_id INTEGER,time INTEGER,  number INTEGER)''')
  db3 = sqlite3.connect("count.sqlite")
  cursor3 = db3.cursor()
  cursor3.execute('''CREATE TABLE IF NOT EXISTS count(countno INTEGER, user_id INTEGER)''''')
  db2.commit()
  cursor2.close()
  db2.close()
  db3.commit()
  cursor3.close()
  db3.close() 
  

  

@client.event
async def on_message(message):
    if message.channel.id == 1165601419508858910:
      data = message.content.split(" ")
      user = re.sub("\D","",data[4])
      user_object = await client.fetch_user(int(user))
      db = sqlite3.connect("eco.sqlite")
      cursor = db.cursor()
      cursor.execute(f"SELECT * FROM eco WHERE user_id = {int(user)}")
      if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO eco VALUES ({int(user)}, 0, 0)")
      cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {int(user)}")
      wallet = cursor.fetchone()
      try:
        wallet = wallet[0]
      except:
        wallet = wallet
      profit = random.randint(500,1000)
      cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ? ",(wallet + profit, int(user)))
      await user_object.send(f"**Thank You For Voting**. You Have Recieved {profit}$")
      db.commit()
      cursor.close()
      db.close()
      
      db2= sqlite3.connect("count.sqlite")
      cursor2 = db2.cursor()
      cursor2.execute(f"SELECT * FROM count")
      if cursor2.fetchone() is None:
          cursor2.execute(f"INSERT INTO count VALUES (0,0)")
      cursor2.execute(f"SELECT countno FROM count WHERE user_id = {int(user)}")
      count = cursor2.fetchone()
      try:
          count = count[0]
      except:
          count = count
      if count != None:
          cursor2.execute(f"UPDATE count SET countno = ? WHERE user_id = ? ",(count + 1, int(user)))
      else:
          cursor2.execute(f"UPDATE count SET countno = ? WHERE user_id = ? ",(1, int(user)))
      db2.commit()
      cursor2.close()
      db2.close()
      db3= sqlite3.connect("vote.sqlite")
      cursor3 = db3.cursor()
      cursor3.execute(f"SELECT * FROM vote WHERE user_id = {int(user)}")
      if cursor3.fetchone() is None:
        if count != None:
            cursor3.execute(f"INSERT INTO vote VALUES ({int(user)},0, {count+1})")
        else:
            cursor3.execute(f"INSERT INTO vote VALUES ({int(user)},0, 1)")
      cursor3.execute("UPDATE vote SET time = ? WHERE user_id = ? ",(datetime.datetime.now().timestamp(), int(user)))
      db3.commit()
      cursor3.close()
      db3.close()
                          
        
    else:
     if not message.author.bot:
      
      if message.guild is None:
        return await client.process_commands(message)
      sb = sqlite3.connect("profanity.sqlite")
      cursor = sb.cursor()
      cursor.execute(f"SELECT enable FROM profanity WHERE guild_id = {message.guild.id}")
      profani = cursor.fetchone()
      try:
        profani = profani[0]
      except:
        profani = profani
      if profani == True:
        if profanity.contains_profanity(message.content):
          await message.delete()
          return await message.channel.send(f"{message.author.mention} You Cannot Use That Word Here!")
      sb.commit()
      cursor.close()
      sb.close()
      
    await client.process_commands(message)



  
    
  


@client.slash_command(name = "meme", description= "Get a meme from reddit")
async def meme(ctx):
  meme_cycle = cycle(['funnymemes', 'memes','meme' , 'dankmemes', 'sadmemes', 'jokememes', 'comedymemes',
      'youtubememes', 'me_irl', 'wholesomememes', 'MemeEconomy', 'AnimalMemes'
  ])
  embed = nextcord.Embed(title="", description="")
  async with aiohttp.ClientSession() as cs:
    async with cs.get(
        f'https://www.reddit.com/r/{next(meme_cycle)}/new.json?') as r:
      res = await r.json()
      embed.set_image(
          url=res['data']['children'][random.randint(0, 15)]['data']['url'])
      await ctx.send(embed=embed)
    

@client.command()
async def wanted(ctx, user : nextcord.Member = None):
  if user == None:
    user = ctx.message.author
  
  wanted = Image.open('wanted.jpg')
  data = BytesIO(await user.display_avatar.read())
  pfp = Image.open(data)
  pfp = pfp.resize((246, 189))
  wanted.paste(pfp,(28,92))

  wanted.save("profile.jpg")
  await ctx.send(file=nextcord.File("profile.jpg"))




def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

@client.command(name= 'restart')
async def restart(ctx):
  if ctx.author.id == OWNER_ID:
    await ctx.send("Restarting bot...")
    restart_bot()
  else:
    return await ctx.send("You don't have permission to use this command")




@client.command(name = "vote",aliases=['v','daily'])
async def vote(ctx):
  embed = nextcord.Embed(title="Vote for us", description="Vote for us on top.gg and discordbotlist.com and get rewards!",color = nextcord.Color.random())
  embed.add_field(name="Top.gg", value="[Click here](https://top.gg/bot/CLIENT_ID/vote)")
  embed.add_field(name="Discordbotlist.com", value="[Click here](https://discordbotlist.com/bots/Client-name/upvote)")
  
  await ctx.send(embed=embed)




@tasks.loop(seconds=30)
async def check():
  db = sqlite3.connect("count.sqlite")
  cursor = db.cursor()
  db2 = sqlite3.connect("vote.sqlite")
  cursor2 = db2.cursor()
  cursor.execute("SELECT * FROM count")
  count = cursor.fetchone()
  if count == None:
    cursor.execute("INSERT INTO count VALUES (?,?)", (0, 0))
  cursor.execute("SELECT countno FROM count")
  countno = cursor.fetchone()
  try:
    countno = countno[0]
  except:
    countno = countno
  for i in range(countno):
    cursor2.execute(f"SELECT * FROM vote WHERE number = {i}")
    vote = cursor2.fetchone()
    if vote == None:
      return
    cursor2.execute("SELECT time FROM vote WHERE number = ?", (i))
    voteno = cursor2.fetchone()
    try:
      voteno = voteno[0]
    except:
      voteno = voteno
    current = datetime.datetime.now().timestamp()
    if current-voteno >= datetime.timedelta(hours=12):
      cursor2.execute("UPDATE vote SET time = ? WHERE number = ?", (0, i))
      cursor2.execute(f"SELECT user_id FROM vote WHERE number = {i}")
      user_id = cursor2.fetchone()
      try:
        user_id = user_id[0]
      except:
        user_id = user_id
      user = client.fetch_user(user_id)
      await user.send(f"Your Vote Timer has been refreshed, please vote again!")
    db2.commit()
  db.commit()
  cursor.close()
  db.close()
  cursor2.close()
  db2.close()
  
    
    
    
  
    
for filename in os.listdir('./cogs'):
   if filename.endswith('.py'):
      client.load_extension(f'cogs.{filename[:-3]}')








client.run(my_secret)