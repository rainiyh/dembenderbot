# bender.py
import os
from discord.ext import commands
import random
import re
import requests
import json
import urllib.parse
from dotenv import load_dotenv
import json

load_dotenv()

# discord bot token
TOKEN = os.getenv('DISCORD_TOKEN')
clashApiToken = os.getenv('CLASH_API_TOKEN')
bot = commands.Bot(command_prefix='!')
clantag = '#9LU8G8LQ' # Clan Dem tag
clantag2 = '#2L89YYJLC' # clan dem #2 tag
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

        # Donations
        elif message.content.startswith('!donations'):
            donations = donationStatsHandling()
            await message.channel.send(donations)
            print("Listed Donations")

# Donations function
def donationStatsHandling():
    # clandem1
    playerData = requests.get(clashApiUrl + urllib.parse.quote_plus(clantag) + '/members', headers = head).json()
    print(playerData)
    # clandem2
    playerDataCD2 = requests.get(clashApiUrl + urllib.parse.quote_plus(clantag2) + '/members', headers = head).json()
    playerDataStr = json.dumps(playerData)
    playerDataStrCD2 = json.dumps(playerDataCD2)
    numOfPlayers = len(re.findall('\\bdonations\\b', playerDataStr))
    numOfPlayersCD2 = len(re.findall('\\bdonations\\b', playerDataStrCD2))
    # Currently all Alt accounts need to be added in manually
    altAccounts = []
    donationString = ''
    donationArray = []
    playerName = ''
    donations = 0
    playerID = 0

    for i in range(0, numOfPlayers):
        playerName = playerData['items'][i]['name']
        donations = playerData['items'][i]['donations']
        playerID = playerData['items'][i]['tag']
        donationArray.append([donations, playerName, playerID])

    for i in range(0, numOfPlayersCD2):
        playerName = playerDataCD2['items'][i]['name']
        donations = playerDataCD2['items'][i]['donations']
        layerID = playerDataCD2['items'][i]['tag']
        donationArray.append([donations, playerName, playerID])

    print(donationArray)

    donationArray.sort(reverse=True)

    donationString += '**Donations:**\n'

    for i in range(0, len(donationArray)):
        donationString += str(donationArray[i][1]) + ": "
        donationString += str(donationArray[i][0]) + '\n'

    return donationString

bot.run(TOKEN)
