import nextcord
from nextcord import user
from nextcord.ext import commands
from nextcord import Interaction
import sqlite3
import re
import random
import time
import datetime
import pickle
import sys
import traceback
from datetime import datetime, timedelta
from typing import Counter
import aiohttp
import humanfriendly
from nextcord.channel import TextChannel
from nextcord.ext import  tasks


class Button(nextcord.ui.View):
  def __init__(self, user):
    super().__init__()
    self.value = None
    self.user = user
  @nextcord.ui.button(label = "Confirm", style = nextcord.ButtonStyle.green)
  async def confirm(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
    if interaction.user.id != self.user:
      return await interaction.response.send_message(content = "This is not your button", ephemeral = True)
    self.value = True
    self.stop()
  @nextcord.ui.button(label = "Cancel", style = nextcord.ButtonStyle.red)
  async def cancel(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
    if interaction.user.id != self.user:
      return await interaction.response.send_message(content = "This is not your button", ephemeral = True)
    self.value = False  
    self.stop()
  
  


class Economy(commands.Cog):

  def __init__(self, client):
    self.client = client

  

  @commands.Cog.listener()
  async def on_ready(self):
    db = sqlite3.connect("eco.sqlite")
    cursor = db.cursor()
    db2= sqlite3.connect("items.sqlite")
    cursor2= db2.cursor()
    db3 = sqlite3.connect("swords.sqlite")
    cursor3 = db3.cursor()
    db4 = sqlite3.connect("fish.sqlite")
    cursor4 = db4.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS eco(user_id INTEGER, wallet INTEGER, bank INTEGER)''')
    cursor2.execute('''CREATE TABLE IF NOT EXISTS items(user_id INTEGER, pistol INTEGER, lootbox INTEGER, fishing_rod INTEGER, pickaxe INTEGER,sword INTEGER, padlock INTEGER)''')
    cursor3.execute('''CREATE TABLE IF NOT EXISTS swords(user_id , wooden_sword INTEGER, stone_sword INTEGER, iron_sword INTEGER, diamond_sword INTEGER)''')
    cursor4.execute('''CREATE TABLE IF NOT EXISTS fish(user_id , fish INTEGER, cod INTEGER, salmon INTEGER, tropical_fish INTEGER, shark INTEGER)''')
    print("Economy is Online")
    db.commit()
    db2.commit()
    db3.commit()
    db4.commit()
    
    
  @commands.command(aliases=["del"])
  async def delete(self, ctx):
    view = Button(ctx.author.id)
    msg = await ctx.send("Are You Sure Want To Delete Your Account",view=view)
    await view.wait()
    if view.value == True:
      await ctx.channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send("Your Account Has Been Deleted, Thank You For Spending So Many Days With Us , Hope You Enjoyed Our Bot")
      db = sqlite3.connect("eco.sqlite")
      db2 = sqlite3.connect("items.sqlite")
      cursor2 = db2.cursor()
      cursor = db.cursor()
      cursor.execute(f"DELETE FROM eco WHERE user_id = {ctx.author.id}")
      db.commit()
      cursor2.execute(f"DELETE FROM items WHERE user_id = {ctx.author.id}")
      db2.commit()
      db3 = sqlite3.connect("fish.sqlite")
      cursor3 = db3.cursor()
      cursor3.execute(f"DELETE FROM fish WHERE user_id = {ctx.author.id}")
      db3.commit()
      
      
      cursor.close()
      db.close()
      
      cursor2.close()
      db2.close()
      
      cursor3.close()
      db3.close()
      
      
    else:
      await ctx.channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send("Ok , Canceled")
      

  
  @commands.command(pass_context=True)
  async def deposit(self,ctx, amount=None):
    if amount == None:
      await ctx.send("Please specify an amount")
      return
    if amount != "all" and amount != "All":
      try:
        temp = int(amount)
      except:
        await ctx.send("Please specify a valid amount")
        return
    db = sqlite3.connect("eco.sqlite")
    cursor= db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    data= cursor.fetchone()
    try:
      wallet= data[1]
      bank= data[2]
    except:
      wallet = 0
      bank = 0
    amount = wallet if amount == "all" or amount=="All" else int(amount)
    if amount>wallet:
      await ctx.send(f"You don't have {amount}$ in your wallet")
      return
    else:
      cursor.execute(f"UPDATE eco SET bank = ? WHERE user_id = ?", (bank+amount, ctx.author.id))
      cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet-amount, ctx.author.id))
      await ctx.send(embed= nextcord.Embed(title="Congrats Weeb", description=f"You deposited {amount}$ into your bank", color=nextcord.Color.random()))
    db.commit()
    cursor.close()
    db.close()
      
  @commands.command(pass_context=True)
  async def withdraw(self,ctx, amount=None):
      if amount == None:
        await ctx.send("Please specify an amount")
        return
      if amount != "all" and amount != "All":
        try:
          temp = int(amount)
        except:
          await ctx.send("Please specify a valid amount")
          return
      db = sqlite3.connect("eco.sqlite")
      cursor= db.cursor()
      cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
      data= cursor.fetchone()
      try:
        wallet= data[1]
        bank= data[2]
      except:
        wallet = 0
        bank = 0
      amount = bank if amount == "all" or amount=="All" else int(amount)
      if amount>bank:
        await ctx.send(f"You don't have {amount}$ in your bank")
        return
      else:
        cursor.execute("UPDATE eco SET bank = ? WHERE user_id = ?", (bank-amount, ctx.author.id))
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet+amount, ctx.author.id))
        await ctx.send(embed= nextcord.Embed(title="Congrats Weeb", description=f"You withdrew {amount}$ from your bank", color=nextcord.Color.random()))
      db.commit()
      cursor.close()
      db.close()
   
  @commands.command(pass_context=True)
  async def start(self,ctx):
    
    db = sqlite3.connect("eco.sqlite")
    db2= sqlite3.connect("items.sqlite")
    cursor2 = db2.cursor()
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {ctx.message.author.id}")
    result = cursor.fetchone()
    cursor2.execute(f"SELECT user_id FROM items WHERE user_id = {ctx.message.author.id}")
    result2 = cursor2.fetchone()
    if result==None and result2==None:
      sql = ("INSERT INTO eco(user_id, wallet, bank) VALUES(?,?,?)")
      val= (ctx.message.author.id, 100, 0)
      cursor.execute(sql,val)
      cursor2.execute("INSERT INTO items(user_id, pistol, lootbox,fishing_rod, pickaxe,sword, padlock) VALUES(?,?,?,?,?,?,?)", (ctx.message.author.id, 0, 1, 1 ,1 ,1, 1))
      await ctx.send("You have started your journey")
    
    elif result2 is None:
      cursor2.execute("INSERT INTO items(user_id, pistol, lootbox,fishing_rod, pickaxe,sword,padlock) VALUES(?,?,?,?,?,?,?)", (ctx.message.author.id, 0, 1, 1, 1, 1, 1))
      await ctx.send(f"You have started your journey")
    elif result is None:
      sql = ("INSERT INTO eco(user_id, wallet, bank) VALUES(?,?,?)")
      val= (ctx.message.author.id, 100, 0)
      cursor.execute(sql,val)
      cursor2.execute("INSERT INTO items(user_id, pistol, lootbox, fishing_rod, pickaxe, sword, padlock) VALUES(?,?,?,?,?,?,?)", (ctx.message.author.id, 0, 1, 1, 1, 1, 1 ))
      await ctx.send(f"You have started your journey")
    else:
      await ctx.send("You already have an account")
      return
    db.commit()
    db2.commit()
    cursor2.close()
    cursor.close()
    db.close()
    db2.close()

  
  @commands.command(aliases=['bal'],pass_context=True)
  async def balance(self,ctx,member: nextcord.Member = None):
    if member is None:
      member = ctx.message.author
    db = sqlite3.connect("eco.sqlite") 
    db2= sqlite3.connect("items.sqlite")
    cursor2= db2.cursor()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    data= cursor.fetchone()
    if data == None:
      return await ctx.send("You Don't have an account first greate one by typing @LuffySama start")
    cursor.execute(f"SELECT wallet,bank FROM eco WHERE user_id = {member.id}")
    bal = cursor.fetchone()
    cursor2.execute(f"SELECT * FROM items WHERE user_id = {member.id}")
    items = cursor2.fetchone()
    try:
      wallet = bal[0]
      bank = bal[1]
      pistol = items[1]
      lootbox = items[2]
      pickaxe = items[3]
    except:
      wallet = 0
      bank = 0
      pistol = 0
      lootbox = 0
      pickaxe = 0
    embed= nextcord.Embed(title=f"Balance",color=nextcord.Color.random())
    embed.add_field(name="Wallet",value=f"{wallet}$")
    embed.add_field(name="Bank",value=f"{bank}$")
    embed.add_field(name="NetWorth", value= f"{wallet+bank}$")
    embed.set_thumbnail(url= "https://static-00.iconduck.com/assets.00/bank-emoji-2048x2002-niu50sk2.png")
    await ctx.send(embed=embed)
    db.commit()
    db2.commit()
    cursor.close()
    cursor2.close()
    db.close()
    db2.close()

  @commands.command(aliases=['inventory'],pass_context=True)
  async def inv(self,ctx,member: nextcord.Member = None):
    if member is None:
      member = ctx.message.author 
    db2 = sqlite3.connect("items.sqlite")
    cursor2 = db2.cursor()
    cursor2.execute(f"SELECT * FROM items WHERE user_id = {ctx.author.id}")
    data= cursor2.fetchone()
    if data == None:
      return await ctx.send("You Don't have an account first greate one by typing @LuffySama start")

    cursor2.execute(f"SELECT * FROM items WHERE user_id = {member.id}")
    items = cursor2.fetchone()
    try:
      pistol = items[1]
      lootbox = items[2]
      pickaxe = items[4]
      fishing_rod = items[3]
      sword = items[5]
      padlock = items[6]
    except:
      pistol = 0
      lootbox = 0
      pickaxe = 0
      fishing_rod = 0
      sword = 0
      padlock = 0
    embed= nextcord.Embed(title=f"Inventory",color=nextcord.Color.random())
    embed.add_field(name="Pistol", value=f"{pistol} owned")
    embed.add_field(name="Lootbox", value=f"{lootbox} owned")
    embed.add_field(name="Pickaxe", value=f"{pickaxe} owned")
    embed.add_field(name="Fishing Rod", value=f"{fishing_rod} owned")
    embed.add_field(name="Sword", value=f"{sword} owned")
    embed.add_field(name="Padlock", value=f"{padlock} owned")
    embed.set_thumbnail(url= "https://cdn-icons-png.flaticon.com/512/831/831698.png")
    await ctx.send(embed=embed)

    db2.commit()
    cursor2.close()
    db2.close()

  

  @commands.command(pass_context= True)
  async def open(self,ctx,amount=None):
    if amount is None:
      amount = 1
    db = sqlite3.connect("items.sqlite") 
    cursor= db.cursor()
    cursor.execute(f"SELECT lootbox FROM items WHERE user_id = {ctx.message.author.id}")
    lootbox= cursor.fetchone()
    try:
      lootbox  = lootbox[0]
    except:
      lootbox = lootbox
    amount = lootbox if amount == "all" or amount == "All" else int(amount)  
    if lootbox == 0:
      await ctx.send("You don't have any lootboxes")
      return
    elif lootbox < amount:
      await ctx.send("You don't have that many lootboxes")
      return
    else:
      cursor.execute(f"SELECT pistol FROM items WHERE user_id = {ctx.message.author.id}")
      pistol = cursor.fetchone()
      try:
        pistol = pistol[0]
      except:
        pistol = pistol
      temp_amount = amount
      pistol_amt = 0  
      rod_amt = 0 
      pickaxe_amt = 0
      nothing_amt = 0
      while temp_amount > 0 :  
        chance= random.randint(0,500)
        if chance <200:
         nothing_amt = nothing_amt+1
        elif chance == 200:
          cursor.execute(f"SELECT pistol FROM items WHERE user_id = {ctx.message.author.id}")
          pistol = cursor.fetchone()
          try:
            pistol = pistol[0]
          except:
            pistol = pistol
          pistol = pistol+1  
          cursor.execute(f"UPDATE items SET pistol = {pistol} WHERE user_id = {ctx.message.author.id}")
          pistol_amt = pistol_amt+1
        elif chance <=300:
          cursor.execute(f"SELECT fishing_rod FROM items WHERE user_id = {ctx.message.author.id}")
          pistol = cursor.fetchone()
          try:
            pistol = pistol[0]
          except:
            pistol = pistol
          cursor.execute(f"UPDATE items SET fishing_rod = {pistol+1} WHERE user_id = {ctx.message.author.id}")
          rod_amt = rod_amt + 1
        else:
          cursor.execute(f"SELECT pickaxe FROM items WHERE user_id = {ctx.message.author.id}")
          pistol = cursor.fetchone()
          try:
            pistol = pistol[0]
          except:
            pistol = pistol
          cursor.execute(f"UPDATE items SET pickaxe = {pistol+1} WHERE user_id = {ctx.message.author.id}")
          pickaxe_amt = pickaxe_amt+1
          
        temp_amount = temp_amount - 1  
      cursor.execute(f"UPDATE items SET lootbox = {lootbox-amount} WHERE user_id = {ctx.message.author.id}")
      await ctx.send(embed = nextcord.Embed(title="Congratulations!",description=f"You Got The Following Items\n\nNothing : x{nothing_amt}\nPistol : x{pistol_amt}\nFishing Rod : x{rod_amt}\nPickaxe : x{pickaxe_amt}",color = nextcord.Color.random()))
    db.commit()
    cursor.close()
    db.close()
    
        
  @commands.command(pass_context=True)
  async def sell(self,ctx, items , amount = None):
    if amount == None:
      amount = 1
    if amount != "all" and amount != "All":
      try:
        temp = int(amount)
      except ValueError:
        await ctx.send("Please enter a valid amount")
        return    
    db = sqlite3.connect("eco.sqlite")
    db2= sqlite3.connect("items.sqlite")
    db3 = sqlite3.connect("fish.sqlite")
    cursor= db.cursor()
    cursor2= db2.cursor()
    cursor3= db3.cursor()
    items = items.lower()
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id ={ctx.author.id}")
    wallet = cursor.fetchone()
    try:
      wallet= wallet[0]
    except:
      wallet = wallet
    if items == "pistol":
      cursor2.execute(f"SELECT pistol FROM items WHERE user_id = {ctx.message.author.id}")
      pistol = cursor2.fetchone()
      try:
        pistol = pistol[0]
      except:
        pistol = pistol
      amount = pistol if amount == "all" or amount =="All" else int(amount)  
      if pistol == 0:
        await ctx.send("You don't have any pistol")
        return
      elif pistol < amount:
        await ctx.send("You don't have that many pistol")
        return
      else:
        cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.message.author.id}")
        cursor.execute("UPDATE eco SET wallet= ? WHERE user_id = ?",(wallet+(amount*100000), ctx.message.author.id))
        embed = nextcord.Embed(title= "Congratulations!", description=f"You sold your pistol for {amount*100000}$",color = nextcord.Color.green())
        await ctx.send(embed=embed)
        cursor2.execute(f"SELECT pistol FROM items WHERE user_id = {ctx.message.author.id}")
        cursor2.execute("UPDATE items SET pistol = ? WHERE user_id = ?",(pistol-amount, ctx.message.author.id))
    elif items == "pickaxe":
      cursor2.execute(f"SELECT pickaxe FROM items WHERE user_id = {ctx.message.author.id}")
      pickaxe = cursor2.fetchone()
      try:
        pickaxe = pickaxe[0]
      except:
        pickaxe = pickaxe
      amount = pickaxe if amount == "all" or amount =="All" else int(amount)  
      if pickaxe == 0:
        await ctx.send("You don't have any pickaxes")
        return
      elif pickaxe < amount:
        await ctx.send("You don't have that many pickaxes")
        return
      else:
        cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.author.id}")
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?",(wallet+(amount*100), ctx.message.author.id))
        embed = nextcord.Embed(title= "Congratulations!", description=f"You sold your pickaxe for {amount*100}$",color = nextcord.Color.red())
        await ctx.send(embed=embed)
        cursor2.execute(f"SELECT pickaxe FROM items WHERE user_id = {ctx.message.author.id}")
        cursor2.execute("UPDATE items SET pickaxe = ? WHERE user_id =?",(pickaxe-amount, ctx.message.author.id))
    elif items == "salmon":
      cursor3.execute(f"SELECT salmon FROM fish WHERE user_id = {ctx.message.author.id}")
      salmon = cursor3.fetchone()
      try:
        salmon = salmon[0]
      except:
        salmon = salmon
      amount = salmon if amount == "all" or amount =="All" else int(amount)  
      if salmon == 0:
        return await ctx.send("You don't have any salmon")
        
      elif salmon < amount:
        return await ctx.send(f"You don't have that many salmon")
      else:
        cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.author.id}")
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?",(wallet+(amount*100), ctx.message.author.id))
        embed = nextcord.Embed(title= "Congratulations!", description=f"You sold your salmon for {amount*100}$",color = nextcord.Color.green())
        await ctx.send(embed=embed)
        cursor3.execute(f"UPDATE items SET salmon = ? WHERE user_id = ?",(salmon-amount, ctx.message.author.id))
    elif items == "shark":
      cursor3.execute(f"SELECT shark FROM fish WHERE user_id = {ctx.message.author.id}")
      shark = cursor3.fetchone()
      try:
        shark = shark[0]
      except:
        shark = shark
      amount = shark if amount == "all" or amount =="All" else int(amount)  
      if shark == 0:
        return await ctx.send("You don't have any sharks")
        
      elif shark < amount:
        return await ctx.send(f"You don't have that many sharks")
      else:
        cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.author.id}")
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?",(wallet+(amount*100000), ctx.message.author.id))
        embed = nextcord.Embed(title= "Congratulations!", description=f"You sold your shark for {amount*100000}$",color = nextcord.Color.green())
        await ctx.send(embed=embed)
        cursor3.execute("UPDATE fish SET shark = ? WHERE user_id = ?",(shark-amount,ctx.author.id))
        
    elif items == "cod":
      cursor3.execute(f"SELECT cod FROM fish WHERE user_id = {ctx.message.author.id}")
      cod = cursor3.fetchone()
      try:
        cod = cod[0]
        
      except:
        cod = cod
      amount = cod if amount == "all" or amount =="All" else int(amount)
      if cod == 0:
        return await ctx.send("You don't have any cod")
        
      elif cod < amount:
        return await ctx.send(f"You don't have that many cod")
      else:
        cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.author.id}")
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?",(wallet+(amount*1000), ctx.message.author.id))
        embed = nextcord.Embed(title= "Congratulations!", description=f"You sold your cod for {amount*1000}$",color = nextcord.Color.green())
        await ctx.send(embed=embed)
        cursor3.execute("UPDATE fish SET cod = ? WHERE user_id = ?",(cod-amount,ctx.author.id))
    elif items == "tropical_fish":
      cursor3.execute(f"SELECT tropical_fish FROM fish WHERE user_id = {ctx.message.author.id}")
      tropical_fish = cursor3.fetchone()
      try:
        tropical_fish = tropical_fish[0]
        
      except:
        tropical_fish = tropical_fish
      amount = tropical_fish if amount == "all" or amount =="All" else int(amount)
      if tropical_fish == 0:
        return await ctx.send("You don't have any tropical fish")
        
      elif tropical_fish < amount:
        return await ctx.send(f"You don't have that many tropical fish")
      else:
        cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.author.id}")
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?",(wallet+(amount*10000), ctx.message.author.id))
        embed = nextcord.Embed(title= "Congratulations!", description=f"You sold your tropical fish for {amount*10000}$",color = nextcord.Color.green())
        await ctx.send(embed=embed)
        cursor3.execute("UPDATE fish SET tropical_fish = ? WHERE user_id = ?",(tropical_fish-amount,ctx.author.id))
    else:
      await ctx.send("You Dont have such an item")
    db.commit()
    db2.commit()
    cursor.close()
    cursor2.close()
    db.close()
    db2.close()
    db3.commit()
    cursor3.close()
    db3.close()
      
        
        
        

        

  @commands.command(pass_context=True)
  @commands.cooldown(1,10,commands.BucketType.user) 
  async def beg(self,ctx):
    
    earnings= random.randint(0,30)
    db= sqlite3.connect("eco.sqlite")
    cursor= db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    data= cursor.fetchone()
    if data == None:
      return await ctx.send("You Don't have an account first greate one by typing @LuffySama start")
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.message.author.id}")
    wallet = cursor.fetchone()
    cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet[0] + int(earnings), ctx.author.id))
    await ctx.send(embed= nextcord.Embed(title="Congratulations Beggar",description=f"You earned **{earnings}$**", color = nextcord.Color.random()))
    db.commit()
    cursor.close()
    db.close()
    
  @commands.command(pass_context=True)
  @commands.cooldown(1,15,commands.BucketType.user) 
  async def dice(self, ctx, amount = None):
    if ctx.message.guild is None:
      return await ctx.send(f"You can't use this command in DMs")
    if(amount == None):
      await ctx.send("Please enter the amount you want to bet")
      return 
    if amount != "all" and amount != "All":
      try:  
        temp = int(amount)
      except ValueError:
        await ctx.send("Please Enter A Number")
        return
    db= sqlite3.connect("eco.sqlite")
    cursor= db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    data= cursor.fetchone()
    if data == None:
      return await ctx.send("You Don't have an account first create one by typing @LuffySama start")
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.message.author.id}")
    wallet = cursor.fetchone()
    try:
      wallet= wallet[0]
    except:
      wallet=wallet

    amount = wallet if amount== "all" or amount=="All" else int(amount)
    if amount > wallet:
      await ctx.send("You don't have enough money to gamble")
      return
    if amount <= 0:
      await ctx.send("Come on Weeb,You can't bet such an amount")
      return
    user_strikes= random.randint(1,6)
    bot_strikes= random.randint(1,6)
    msg = await ctx.send("The Dice have been rolled 🎲🎲.....")
    time.sleep(5)
    if user_strikes > bot_strikes:
      cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + int(amount), ctx.author.id))
      embed= nextcord.Embed(description=f"You Won!. {(2*amount)}$ has been returned to your wallet" , color= nextcord.Color.random())
      embed.add_field(name = ctx.author.name, value=f"You Rolled a {user_strikes}")
      embed.add_field(name= "Bot", value= f"I Rolled a {bot_strikes} ")
      if ctx.author.avatar != None:
        embed.set_author(name= ctx.author.name, icon_url= ctx.author.avatar.url)
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed=embed)
    elif user_strikes == bot_strikes:
      embed= nextcord.Embed(description=f"You Tied {amount}$ has been returned to your wallet" , color= nextcord.Color.random())
      if ctx.author.avatar != None:
        embed.set_author(name= ctx.author.name, icon_url= ctx.author.avatar.url)
      embed.add_field(name= ctx.author.name, value = f"You rolled a {user_strikes}")
      embed.add_field(name= "Bot", value = f"I rolled a {bot_strikes}")
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed=embed)
    else:
      cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))
      embed= nextcord.Embed(description=f"You Lost {amount}$ has been taken from your wallet", color= nextcord.Color.random())
      if ctx.author.avatar != None:
        embed.set_author(name = ctx.author.name, icon_url= ctx.author.avatar.url)
      embed.add_field(name= ctx.author.name, value = f"You Rolled a {user_strikes}")
      embed.add_field(name= "Bot", value = f"I rolled a {bot_strikes}")
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed=embed)


    db.commit()
    cursor.close()
    db.close()

  @commands.command(aliases = ["coinflip",'CF',"cF","Cf"],pass_context=True)
  @commands.cooldown(1,15,commands.BucketType.user) 
  async def cf(self, ctx, side , amount = None):
    if ctx.message.guild is None:
      return await ctx.send("You can't use this command in DMs")
    if(amount == None):
      await ctx.send("Please enter the amount you want to bet")
      return 
    if amount != "all":
      try:  
        temp = int(amount)
      except ValueError:
        await ctx.send("Please Enter A Number")
        return
    
    db = sqlite3.connect("eco.sqlite")
    cursor= db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    data= cursor.fetchone()
    if data == None:
      return await ctx.send("You Don't have an account first create one by typing @LuffySama start")
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.message.author.id}")
    wallet = cursor.fetchone()
    try:
      wallet= wallet[0]
    except:
      wallet= wallet
    amount = wallet if amount == "all" else int(amount)
    if amount > wallet:
      await ctx.send("You don't have that much money to gamble")
      return
    if amount <= 0:
      await ctx.send(f"Come on Weeb,You can't bet such an amount")
      return
    coin= random.randint(1,2)
    msg = await ctx.send("The Coin has been flipped 🪙🪙 **..........**")
    time.sleep(5)
    
    if side == "heads":
      if coin == 1:
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + int(amount), ctx.author.id))
        embed= nextcord.Embed(description=f"You Won!. {(2*amount)}$ has been given to your wallet" , color= nextcord.Color.random())
        embed.add_field(name= ctx.author.name, value= "Heads" )
        channel = ctx.channel
        await channel.purge(limit=1, check=lambda message: msg.id == message.id)
        await ctx.send(embed=embed)
      else:
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - int(amount), ctx.author.id))
        embed= nextcord.Embed(description=f"You Lost {amount}$ has been taken from your wallet", color= nextcord.Color.random())
        embed.add_field(name= ctx.author.name, value = "Tails")
        channel = ctx.channel
        await channel.purge(limit=1, check=lambda message: msg.id == message.id)
        await ctx.send(embed=embed)
    elif side == "tails":
      if coin == 2:
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + amount, ctx.author.id))
        embed= nextcord.Embed(description=f"You Won!. {(2*amount)}$ has been returned to your wallet" , color= nextcord.Color.random())
        embed.add_field(name= ctx.author.name, value= "Tails" )
        channel = ctx.channel
        await channel.purge(limit=1, check=lambda message: msg.id == message.id)
        await ctx.send(embed=embed)
      else:
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))
        embed= nextcord.Embed(description=f"You Lost {amount}$ has been taken from your wallet", color= nextcord.Color.random())
        embed.add_field(name= ctx.author.name, value = "Heads")
        channel = ctx.channel
        await channel.purge(limit=1, check=lambda message: msg.id == message.id)
        await ctx.send(embed=embed)
    elif side == "t":
      if coin == 2:
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + amount, ctx.author.id))
        embed= nextcord.Embed(description=f"You Won!. {(2*amount)}$ has been returned to your wallet" , color= nextcord.Color.random())
        embed.add_field(name= ctx.author.name, value= "Tails" )
        channel = ctx.channel
        await channel.purge(limit=1, check=lambda message: msg.id == message.id)
        await ctx.send(embed=embed)
      else:
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))
        embed= nextcord.Embed(description=f"You Lost {amount}$ has been taken from your wallet", color= nextcord.Color.random())
        embed.add_field(name= ctx.author.name, value = "Heads")
        channel = ctx.channel
        await channel.purge(limit=1, check=lambda message: msg.id == message.id)
        await ctx.send(embed=embed)
    elif side == "h":
      if coin == 1:
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + int(amount), ctx.author.id))
        embed= nextcord.Embed(description=f"You Won!. {(2*amount)}$ has been returned to your wallet" , color= nextcord.Color.random())
        embed.add_field(name= ctx.author.name, value= "Heads" )
        channel = ctx.channel
        await channel.purge(limit=1, check=lambda message: msg.id == message.id)
        await ctx.send(embed=embed)
      else:
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - int(amount), ctx.author.id))
        embed= nextcord.Embed(description=f"You Lost {amount}$ has been taken from your wallet", color= nextcord.Color.random())
        embed.add_field(name= ctx.author.name, value = "Tails")
        channel = ctx.channel
        await channel.purge(limit=1, check=lambda message: msg.id == message.id)
        await ctx.send(embed=embed)
    else:
      await ctx.send("Please Enter a valid side")
      return
    db.commit()
    cursor.close()
    db.close()
    
  
  
  @commands.command(pass_context= True)
  @commands.cooldown(1,15,commands.BucketType.user) 
  async def slots(self, ctx, amount = None):
    if ctx.message.guild is None:
      return await ctx.send("This command is not allowed in DMs")
    if amount == None:
      await ctx.send("Please Enter the amount to bet")
      return
    if amount != "all" and amount != "All":
      try:
        temp= int(amount)
      except ValueError:
        await ctx.send("Please Enter a valid amount")
        return
      
    db = sqlite3.connect("eco.sqlite")
    cursor= db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    data= cursor.fetchone()
    if data == None:
      return await ctx.send("You Don't have an account first create one by typing @LuffySama start")
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.author.id}")
    wallet = cursor.fetchone()
    try:
      wallet=wallet[0]
    except:
      wallet=wallet
      
    amount = wallet if amount == "all" or amount=="All" else int(amount)
    
    if amount>wallet:
      embed = nextcord.Embed(title= ctx.author.name,description=f"You don't have enough money to bet {amount}$", color= nextcord.Color.random())
      await ctx.send(embed=embed)
      return
    if amount<=0:
      await ctx.send("Come on Weeb,You can't bet such an amount")
      return
    times_factors = random.randint(1,5)
    earning = int(amount*times_factors)
    final = []
    for i in range(3):
      a = random.choice(["🍉","💎","💰"])
      final.append(a)
    msg = await ctx.send("Waiting For Slot Machine........")
    
    time.sleep(5)
    if final[0] == final[1] and final[1] == final[2]:
      cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + earning, ctx.author.id))
      embed= nextcord.Embed(title=f"Slots Machine", color= nextcord.Color.green())
      embed.add_field(name=f"You Won 💸{earning}$", value=f"{final}")
      embed.add_field(name=f"----------------------------------", value=f"**Multiplier** x{times_factors}", inline= False)
      embed.add_field(name=f"----------------------------------", value=f"**New Balance** 💸{wallet+earning}$", inline= False)
      embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed=embed)
    else:
      cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - earning, ctx.author.id))
      embed= nextcord.Embed(title=f"Slots Machine", color= nextcord.Color.green())
      embed.add_field(name=f"You Lost 💸{earning}$", value=f"{final}")
      embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed=embed)
    db.commit()
    cursor.close()
    db.close()


  @commands.command(pass_context=True)
  @commands.cooldown(1,15,commands.BucketType.user) 
  async def send(self,ctx,member : nextcord.Member = None, amount = None):
    if amount == None:
      return await ctx.send("Please Specify The Amount You Want To Send")
    elif member == None:
      return await ctx.send("Please Specify The Member To Whom You want to send the money")
    db = sqlite3.connect("eco.sqlite")
    cursor= db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    data= cursor.fetchone()
    if data == None:
      return await ctx.send("You Don't have an account first create one by typing zoro start")
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {member.id}")
    data= cursor.fetchone()
    if data == None:
      return await ctx.send("Your friend Doesn't have an account first tell him to create one by typing @LuffySama start")
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.author.id}")
    user_wallet= cursor.fetchone()
    try:
      user_wallet = user_wallet[0]
    except:
      user_wallet= user_wallet
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {member.id}")
    member_wallet= cursor.fetchone()
    try :
      member_wallet = member_wallet[0]
    except:
      member_wallet = member_wallet
    view = Button(ctx.author.id)
    msg = await ctx.send(f"Are You Sure You Want To Give This Amount To {member.mention}", view=view)
    await view.wait()
    
    amount = user_wallet if amount == "all" or amount == "All" else int(amount)
    if view.value == None:
      return
    elif view.value == True:
      if amount > user_wallet:
        return await ctx.send("You don't have enough money to send")
      elif amount <= 0:
        return await ctx.send("Come on Weeb,You can't send such an amount")
      cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (user_wallet-amount, ctx.author.id))
      cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (member_wallet+amount, member.id))
      embed= nextcord.Embed(title="Money Transfer", description = f"{ctx.author.mention} send {amount}$ to {member.mention}", color= nextcord.Color.random())
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed=embed)
    else:
      return await ctx.send("You Declined The Request")
    db.commit()
    cursor.close()
    db.close()


  @commands.command(pass_context=True)
  @commands.cooldown(1,15,commands.BucketType.user) 
  async def rob(self,ctx,member: nextcord.Member = None, amount = None):
    if amount == None:
      return await ctx.send("Please Specify The Amount You Want To Rob")
    elif member == None:
      return await ctx.send("Please Specify The Member To Whom You want to rob")
    db = sqlite3.connect("eco.sqlite")
    if amount != "all" and amount != "All":
      try:
        temp = int(amount)
      except ValueError:
        return await ctx.send("Please Specify The Amount Correctly")
    cursor= db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    if cursor.fetchone() is None:
      return await ctx.send("You Don't have an account first create one by typing @LuffySama start")
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {member.id}")
    if cursor.fetchone() is None:
      return await ctx.send("Your friend Doesn't have an account first tell him to create one by typing @LuffySama start")
      
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.author.id}")
    user_wallet= cursor.fetchone()
    try:
      user_wallet = user_wallet[0]
    except:
      user_wallet = user_wallet
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {member.id}")
    member_wallet = cursor.fetchone()
    try:
      member_wallet = member_wallet[0]
    except:
      member_wallet = member_wallet
    
    if member_wallet <=0:
      return await ctx.send("Weeb, He is poor leave him he doesn't even have a dollar")
    amount = member_wallet if amount == "all" or amount == "All" else int(amount)
    if amount > member_wallet:
      return await ctx.send("He doesn't have that much money")
    chance = random.randint(1,3)
    msg = await ctx.send("Robbery is taking place 🤫🤫 ......")
    time.sleep(5)
    if chance == 2:
      embed = nextcord.Embed(title = "Congratulations" , description = f"You Robbed {member.mention} and got {amount}$",color = nextcord.Color.random())
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed = embed)
      cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (member_wallet-amount, member.id))
      cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (user_wallet+amount, ctx.author.id))
    else:
      embed = nextcord.Embed(title = "You Failed" , description = f"You Failed To Rob {member.mention}, {amount}$ have been cut from your account as fine",color = nextcord.Color.random())
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed = embed)
      cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (user_wallet-amount, ctx.author.id))
    db.commit()
    cursor.close()
    db.close()
    
  @commands.command(pass_context=True)
  async def shop(self,ctx):
    db = sqlite3.connect("eco.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    if cursor.fetchone() is None:
      return await ctx.send("You Don't have an account first create one by typing zoro start")
    embed = nextcord.Embed(title = "Shop", color = nextcord.Color.blue(),description="Please specify the item to buy by typing @LuffySama buy >item number<\n1. Pistol - 100000$\n2. Fishing Rod - 1000$\n3. Sword - 2000$\n4. Padlock - 1000$")
    await ctx.send(embed = embed)
    db.commit()
    cursor.close()
    db.close()
    
  @commands.command(pass_context=True)
  async def buy(self , ctx , itemss = None, amount = None):
    if amount is None:
      amount = 1
    try:
        temp = int(amount)
    except ValueError:
        return await ctx.send("Please Specify The Amount Correctly")
    try:
        temp = int(itemss)
    except ValueError:
        return await ctx.send("Please Specify The Item By Their Number Correctly")
    author = ctx.author.id  
    itemss = int(itemss) 
    amount = int(amount)
    db = sqlite3.connect("eco.sqlite")
    db2 = sqlite3.connect("items.sqlite")
    cursor = db.cursor()
    cursor2 = db2.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    if cursor.fetchone() is None:
      return await ctx.send("You Don't have an account first create one by typing @LuffySama start")
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {ctx.author.id}")
    cursor2.execute(f"SELECT * FROM items WHERE user_id = {ctx.author.id}")
    user_wallet = cursor.fetchone()
    item = cursor.fetchone()
    try:
      user_wallet = user_wallet[0]
    except:
      user_wallet= user_wallet
      
    if itemss is None:
      return await ctx.send("Please specify the item to buy by typing @LuffySama buy >item number<")
    elif itemss == 1:
      if user_wallet < 100000*amount:
        return await ctx.send("You Don't Have Enough Money")
      else:
        view = Button(ctx.author.id)
        msg = await ctx.send("Are You Sure You Want To Buy This Item", view = view)
        await view.wait()
        if view.value == True:
          cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (user_wallet-100000*amount, author))
          cursor2.execute(f"SELECT pistol FROM items WHERE user_id = {author}")
          pistol = cursor2.fetchone()
          try:
            pistol = pistol[0]
          except:
            pistol = 0
          cursor2.execute("UPDATE items SET pistol = ? WHERE user_id = ?", (pistol + amount, author))
          await ctx.channel.purge(limit=1, check=lambda message: msg.id == message.id)
          await ctx.send(embed = nextcord.Embed(title = "Purchase Successful", description = f"You Bought {amount} Pistol(s)",color = nextcord.Color.green()))
        else:
          await ctx.channel.purge(limit=1, check=lambda message: msg.id == message.id)
          await ctx.send("Purchase Cancelled")
    elif itemss == 2:
      if user_wallet < 1000*amount:
        return await ctx.send("You Don't Have Enough Money")
      else:
        view = Button(ctx.author.id)
        msg = await ctx.send("Are You Sure You Want To Buy This Item", view = view)
        await view.wait()
        if view.value == True:
          cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (user_wallet-1000*amount, ctx.author.id))
          cursor2.execute(f"SELECT fishing_rod FROM items WHERE user_id = {ctx.author.id}")
          fishing_rod = cursor2.fetchone()
          try:
            fishing_rod = fishing_rod[0]
          except:
            fishing_rod = 0
          cursor2.execute(f"UPDATE items SET fishing_rod = ? WHERE user_id = ?",(fishing_rod + amount, author))
          await ctx.channel.purge(limit=1, check=lambda message: msg.id == message.id)
          await ctx.send(embed = nextcord.Embed(title = "Purchase Successful", description = f"You Bought {amount} Fishing Rod(s)",color = nextcord.Color.green()))
          
        else:
          await ctx.channel.purge(limit=1, check=lambda message: msg.id == message.id)
          await ctx.send("Purchase Cancelled")
    elif itemss == 3:
      if user_wallet < 2000*amount:
        return await ctx.send("You Don't Have Enough Money")
      else:
        view = Button(ctx.author.id)
        msg = await ctx.send("Are You Sure You Want To Buy This Item", view = view)
        await view.wait()
        if view.value == True:
          cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (user_wallet-2000*amount, author))
          cursor2.execute(f"SELECT sword FROM items WHERE user_id = {ctx.author.id}")
          sword = cursor2.fetchone()
          try:
            sword = sword[0]
            
          except:
            sword = 0
          cursor2.execute(f"UPDATE items SET sword = ? WHERE user_id = ?",(sword + amount, author))
          await ctx.channel.purge(limit=1, check=lambda message: msg.id == message.id)
          await ctx.send(embed = nextcord.Embed(title = "Purchase Successful", description = f"You Bought {amount} Sword(s)",color = nextcord.Color.green()))
        else:
          await ctx.channel.purge(limit=1, check=lambda message: msg.id == message.id)
          await ctx.send("Purchase Cancelled")
    elif itemss == 4:
      if user_wallet < 1000*amount:
        return await ctx.send("You Don't Have Enough Money")
      else:
        view = Button(ctx.author.id)
        msg = await ctx.send("Are You Sure You Want To Buy This Item", view = view)
        await view.wait()
        if view.value == True:
          cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (user_wallet-1000*amount, author))
          cursor2.execute(f"SELECT padlock FROM items WHERE user_id = {ctx.author.id}")
          padlock = cursor2.fetchone()
          try:
            padlock = padlock[0]
          except:
            padlock = 0
          cursor2.execute("UPDATE items SET padlock = ? WHERE user_id = ?", (padlock + amount, ctx.author.id))
          await ctx.channel.purge(limit=1, check=lambda message: msg.id == message.id)
          await ctx.send(embed = nextcord.Embed(title = "Purchase Successful", description = f"You Bought {amount} Padlock(s)",color = nextcord.Color.green()))
        else:
          await ctx.channel.purge(limit=1, check=lambda message: msg.id == message.id)
          await ctx.send("Purchase Cancelled")
    else:
      await ctx.send("Invalid Item")
      
    db.commit()
    db2.commit()
    cursor.close()
    cursor2.close()
    db.close()
    db2.close()

  @commands.command(pass_context=True)
  @commands.cooldown(1,15,commands.BucketType.user)  
  async def fish(self, ctx):
    if ctx.message.guild is None:
      return await ctx.send("This Command Is Not Allowed In DMs")
    db = sqlite3.connect("items.sqlite")
    db2 = sqlite3.connect("fish.sqlite")
    cursor = db.cursor()
    cursor2 = db2.cursor()
    cursor.execute(f"SELECT fishing_rod FROM items WHERE user_id = {ctx.author.id}")
    cursor2.execute(f"SELECT * FROM fish WHERE user_id = {ctx.author.id}")
    if cursor2.fetchone() is None:
      cursor2.execute(f"INSERT INTO fish VALUES (?, ?, ?, ?, ?, ?)",(ctx.author.id, 0, 0, 0, 0, 0))
    fishing_rod = cursor.fetchone()
    try:
      fishing_rod = fishing_rod[0]
    except:
      fishing_rod = fishing_rod
    if fishing_rod == 0:
      return await ctx.send(f"You Don't Have A Fishing Rod, Buy One From The Shop or You Can Get One From LootBox")
      
    cursor2.execute(f"SELECT fish FROM fish WHERE user_id = {ctx.author.id}")  
    fish = cursor2.fetchone()
    try:
      fish = fish[0]
      
    except:
      fish = fish

    chance = random.randint(0,100) 
    msg = await ctx.send("Fishing🎣🎣......")
    time.sleep(5)
    if chance == 100:
      cursor.execute(f"SELECT padlock FROM items WHERE user_id = {ctx.author.id}")
      padlock = cursor.fetchone()
      try:
        padlock = padlock[0]
      except:
        padlock = padlock
      padlock = int(padlock)
      if padlock == 0:
        return await msg.edit(content = "You Don't Have A Padlock, Buy One From The Shop or You Can Get One From LootBox")
      cursor.execute(f"SELECT padlock FROM items WHERE user_id = {ctx.author.id}" )
      cursor.execute(f"UPDATE items SET padlock = ? WHERE user_id = ?", (padlock - 1, ctx.author.id))
      cursor.execute("UPDATE items SET fishing_rod = ? WHERE user_id = ?",(fishing_rod - 1, ctx.author.id))
      embed = nextcord.Embed(title = "You Fished", description = f"You Caught A Shark", color = nextcord.Color.green())
      cursor2.execute("UPDATE fish SET fish = ? WHERE user_id = ?", (fish + 1, ctx.author.id))
      cursor2.execute("SELECT shark FROM fish WHERE user_id = ?", (ctx.author.id))
      
      cursor2.execute("UPDATE fish SET shark = ? WHERE user_id = ?", (fish + 1, ctx.author.id))
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed= embed)

    elif chance <100 and chance>50:
      cursor.execute(f"SELECT padlock FROM items WHERE user_id = {ctx.author.id}")
      padlock = cursor.fetchone()
      try:
        padlock = padlock[0]
      except:
        padlock = padlock
      if padlock == 0:
        return await msg.edit(content="You Don't Have A Padlock, Buy One From The Shop or You Can Get One From LootBox")
      cursor.execute(f"SELECT padlock FROM items WHERE user_id = {ctx.author.id}")
      cursor.execute(f"UPDATE items SET padlock = ? WHERE user_id = ?", (padlock-1, ctx.author.id))
      cursor.execute("UPDATE items SET fishing_rod = ? WHERE user_id = ?",(fishing_rod - 1, ctx.author.id))
      embed = nextcord.Embed(title = "You Fished", description = f"You Caught a salmon", color = nextcord.Color.red())
      cursor2.execute("UPDATE fish SET fish = ? WHERE user_id = ?", (fish + 1, ctx.author.id))
      cursor2.execute(f"SELECT salmon FROM fish WHERE user_id = {ctx.author.id}")
      salmon = cursor2.fetchone()
      try:
        salmon = salmon[0]
      except:
        salmon = salmon

      cursor2.execute("UPDATE fish SET salmon = ? WHERE user_id = ?", (salmon + 1, ctx.author.id))
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed = embed)
      
    elif chance <=50 and chance>10:
      cursor.execute(f"SELECT padlock FROM items WHERE user_id = {ctx.author.id}")
      padlock = cursor.fetchone()
      try:
        padlock = padlock[0]
      except:
        padlock = padlock
      padlock = int(padlock)  
      if padlock == 0:
        return await msg.edit(content="You Don't Have A Padlock, Buy One From The Shop or You Can Get One From LootBox")
      cursor.execute(f"SELECT padlock FROM items WHERE user_id = {ctx.author.id}")
      cursor.execute(f"UPDATE items SET padlock = ? WHERE user_id = ? ", (padlock - 1, ctx.author.id))
      cursor.execute("UPDATE items SET fishing_rod = ? WHERE user_id = ?",(fishing_rod - 1, ctx.author.id))
      embed = nextcord.Embed(title = "You Fished", description = f"You Caught a cod" , color = nextcord.Color.blue())
      cursor2.execute("UPDATE fish SET fish = ? WHERE user_id = ?", (fish + 1, ctx.author.id))
      cursor2.execute(f"SELECT cod FROM fish WHERE user_id = {ctx.author.id}")
      cod = cursor2.fetchone()
      try:
        cod = cod[0]
        
      except:
        cod = cod
      cursor2.execute("UPDATE fish SET cod = ? WHERE user_id = ?", (cod + 1, ctx.author.id))
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed = embed)
    elif chance > 5:
      cursor.execute(f"SELECT padlock FROM items WHERE user_id = {ctx.author.id}")
      padlock = cursor.fetchone()
      try:
        padlock = padlock[0]
      except:
        padlock = padlock
      padlock = int(padlock)
      if padlock == 0:
        return await msg.edit(content="You Don't Have A Padlock, Buy One From The Shop or You Can Get One From LootBox")
      cursor.execute(f"SELECT padlock FROM items WHERE user_id = {ctx.author.id}")
      cursor.execute(f"UPDATE items SET padlock = ? WHERE user_id = ?", (padlock-1, ctx.author.id))
      cursor.execute("UPDATE items SET fishing_rod = ? WHERE user_id = ?",(fishing_rod - 1, ctx.author.id))
      embed = nextcord.Embed(title = "You Fished", description = f"You Caught a tropical fish" , color = nextcord.Color.green())
      cursor2.execute("UPDATE fish SET fish = ? WHERE user_id = ?", (fish+1, ctx.author.id))
      cursor2.execute(f"SELECT tropical_fish FROM fish WHERE user_id = {ctx.author.id}")
      tropical_fish = cursor2.fetchone()
      try:
        tropical_fish = tropical_fish[0]
        
      except:
        tropical_fish = tropical_fish
      cursor2.execute("UPDATE fish SET tropical_fish = ? WHERE user_id = ?", (tropical_fish + 1, ctx.author.id))
      channel = ctx.channel
      await channel.purge(limit=1, check=lambda message: msg.id == message.id)
      await ctx.send(embed = embed)

    else:
      await ctx.send("You Caught Nothing")
    db.commit()
    cursor.close()
    db.close()
    db2.commit()
    cursor2.close()
    db2.close()


        
  @commands.Cog.listener()
  async def on_command_error(self,ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
      msg = '**Still On CoolDown**, please try again in `{:.2f} s`'.format(error.retry_after)
      await ctx.send(msg)
  
    
def setup(client):
  client.add_cog(Economy(client))