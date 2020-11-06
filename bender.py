# bender.py
import os
from discord.ext import commands
import random
import re
import requests
import json
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

# discord bot token
TOKEN = os.getenv('DISCORD_TOKEN')
clashApiToken = os.getenv('CLASH_API_TOKEN')
bot = commands.Bot(command_prefix='!')
clantag = '#9LU8G8LQ' # Clan Dem tag
clashApiUrl = 'https://api.clashofclans.com/v1/clans/'
headers = {'content-type': 'application/json'}
head = {'Authorization': 'Bearer {}'.format(clashApiToken)}


# display success message on connection
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.event
async def on_message(message):
    if not message.author.bot:
        # defend self
        if 'bot sucks' in message.content or 'bot sux' in message.content or 'bender, you suck' in message.content or 'you, bender' in message.content or 'you bender' in message.content:
            response = 'Bite my shiny metal ass.'
            await message.channel.send(response)
        
        # explain self
        elif message.content == '!hi' or message.content == '!bot':
            response = 'I am Bender. Please insert girder.'
            await message.channel.send(response)
        
        # call out stallers
        elif 'not stall' in message.content or "i didn't stall" in message.content.lower() or 'i didnt stall' in message.content.lower():
            response = 'Ok, staller'
            await message.channel.send(response)
        
        # toss coin
        elif message.content == 'toss a coin':
            if (random.randint(0, 1) == 1):
                response = 'heads'
            else:
                response = 'tails'
            await message.channel.send(response)
        
        # roll dice
        elif message.content.startswith('!roll'):
            roll = re.search('(\d+)?d(\d+)', message.content)
            if (roll):
                p = re.compile('\d+')
                parsedNumbers = p.findall(roll.group())
                numDice = int(parsedNumbers[0])
                diceType = int(parsedNumbers[1])
                sum = 0
                for i in range(0, numDice):
                    sum += random.randint(1, diceType)
                response = sum
            else:
                response = 'Bad syntax'
            await message.channel.send(response)
    
        # API request
        elif message.content.startswith ('!get'):
            dataResponse = requests.get(clashApiUrl + urllib.parse.quote_plus(clantag), headers = head)
            jsonResponse = dataResponse.json()
            print(jsonResponse)
                
bot.run(TOKEN)

