from aiohttp import client
import nextcord , asyncio , datetime
from nextcord.ext import commands



class Moderation(commands.Cog):

  def __init__(self, client):
    self.client = client
  @commands.command(pass_context=True)
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: nextcord.Member, *, reason=None):


     if reason == None:
      reason = "Being Dumb"

     if member == ctx.message.author:
      embed1= nextcord.Embed(color = nextcord.Color.random(), title = "So Sad", description= "You can't kick yourself")
      await ctx.send(embed=embed1)
     elif member== member.guild_permissions.administrator:
      embed7= nextcord.Embed(color = nextcord.Color.random(), title = "So Sad", description= "You can't kick an administrator")
      await ctx.send(embed=embed7)

     else:

      await ctx.guild.kick(member)
      embed2 = nextcord.Embed(color = nextcord.Color.random(), title = "Task Done", description= f"{member.mention} has been kicked by {ctx.message.author.mention} for {reason}")
      await ctx.send(embed=embed2)
      await member.send(f"You have been kicked from {ctx.guild.name} for {reason}")



  @kick.error
  async def kick_error(self, ctx, error):
     if isinstance(error, commands.MissingPermissions):
       embed3 = nextcord.Embed(color = nextcord.Color.random(), title = "So Sad", description= "You don't have permission to kick someone")
       await ctx.send(embed=embed3)

  @commands.command(pass_context= True, description="Bans The Server Member Specified ")
  @commands.has_permissions(kick_members=True)
  async def ban(self,ctx, member: nextcord.Member, *, reason=None):
     if reason == None:
       reason = "Being Dumb"

     if member == ctx.message.author:
       embed4= nextcord.Embed(color = nextcord.Color.random(), title = "So Sad", description= "You can't ban yourself")
       await ctx.send(embed=embed4)

     elif member== member.guild_permissions.administrator:
      embed8= nextcord.Embed(color = nextcord.Color.random(), title = "So Sad", description= "You can't ban an administrator")
      await ctx.send(embed=embed8)
     else:

      await ctx.guild.ban(member)
      embed5 = nextcord.Embed(color =nextcord.Color.random(), title = "Task Done", description= f"{member.mention} has been banned by {ctx.message.author.mention} for {reason}")
      await ctx.send(embed=embed5)
      await member.send(f"You have been banned from {ctx.guild.name} for {reason}")

  @ban.error
  async def ban_error(self,ctx, error):
     if isinstance(error, commands.MissingPermissions):
      embed6 = nextcord.Embed(color = nextcord.Color.random(), title = "So Sad", description= "You don't have permission to ban someone")
      await ctx.send(embed=embed6)

 
  @commands.command(pass_context= True,alliases="membercount")
  async def members(self,ctx):
   embed = nextcord.Embed(title="Members", description=f"There are {ctx.guild.member_count} members in this server", color=nextcord.Color.random())
    
   await ctx.send(embed=embed)
    
  @commands.command(pass_context= True, aliases = ['purge','p','c'])
  @commands.has_permissions(manage_messages = True)
  async def clear(self,ctx: commands.Context, limit = None):
    if ctx.channel.type == nextcord.ChannelType.text:
      if limit  == None:
        limit = 2
      try:
        limit = int(limit)
      except ValueError:
        await ctx.send("Please enter a valid number")
        return
      if limit>100:
        await ctx.send("Sorry We Can't Delete So Many Messages At One Time Or Else We Will Be Rate Limited")
        return
      await asyncio.sleep(1)
      await ctx.channel.purge(limit=limit+1)
      purge_embed = nextcord.Embed(title='Clear', description=f'Successfully cleared {limit} messages. \n Command executed by {ctx.author}.', color=nextcord.Colour.random())
      await ctx.channel.send(embed=purge_embed, delete_after= 10)
    else:
      await ctx.send("This command can only be used in a text channel.")
      return

  @clear.error
  async def clear_error(self,ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have permissions to clear messages")


  




def setup(client):
     client.add_cog(Moderation(client))