#IMPORT LIBRARIES

import discord
import os
import requests
import json
from discord.ext import commands
from keep_alive import keep_alive
from replit import db
import datetime
import pytz
import time

client = commands.Bot(command_prefix="!", case_insensitive=True)

#DEFINE FUNCTIONS

def get_insult(who):
  params = {"who":who}
  response = requests.get("https://insult.mattbas.org/api/insult.json?who=", params=params)
  json_data = json.loads(response.text)
  insult = json_data ['insult']
  return(insult)

def get_joke():
  url = "https://icanhazdadjoke.com"  
  response = requests.get(url, headers={"Accept": "application/json"})
  json_data = json.loads(response.text)
  joke = json_data["joke"]
  return(joke)

  
#EVENTS
  
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

#COMMANDS
  
@client.command()
async def insult(ctx,arg):
  await ctx.send(get_insult(arg))

@client.command()
async def timezone(ctx,arg):
  response = db[arg]["timezone"]
  await ctx.send(arg + "'s timezone is " + response)
  time_now_zone = datetime.datetime.now(pytz.timezone(response))
  dt_string = time_now_zone.strftime("%d/%m/%Y %H:%M:%S")
  await ctx.send("Current time over there: " + dt_string)
  
@client.command()
async def location(ctx,arg):
  response = db[arg]["location"]
  await ctx.send(arg + "'s location is " + response)

@client.command()
async def joke(ctx):
  await ctx.send(f"Here comes a dad joke:\n{get_joke()}")

@client.command()
async def add_user(ctx, *args):
  if args[0] in db.keys():
    await ctx.send(f"{args[0]} is already in database.")
    await ctx.send(db[args[0]])
  else:
    db[args[0].lower()] = {"timezone":args[1], "location": args[2]}
    await ctx.send(f"Added {args[0].lower()} to database.")
    await ctx.send(db[args[0].lower()])

@client.command()
async def del_user(ctx, arg):
  arg = arg.lower()
  if arg in db.keys():
    del db[arg]
    await ctx.send(f"{arg} has been deleted from database.")
  else:
    await ctx.send(f"{arg} is not in database.")
  
@client.command()
async def list_user(ctx, *args):  
  for arg in args:
    arg = arg.lower()
    if arg in db.keys():
      await ctx.send(f"{arg}:\n{db[arg]}")
    else:
      await ctx.send(f"{arg}:\n{arg} is not in database.")

@client.command()
async def list_all(ctx):
  keys = sorted(db.keys())
  await ctx.send(f"There are {len(db.keys())} entries in the database.\n{keys}") 
      
      

  
#run stuff-----------------------------------------------------------------------
keep_alive()  
my_secret = os.environ['TOKEN']
client.run(my_secret)

