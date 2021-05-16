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

        elif message.content == '!help':
            response = '`!donations`: List donations'
            await message.channel.send(response)

        # explain self
        elif message.content == '!hi' or message.content == '!bot':
            response = 'I am Bender. Please insert girder.'
            await message.channel.send(response)

        # call out stallers
        elif 'not stall' in message.content or "i didn't stall" in message.content.lower() or 'i didnt stall' in message.content.lower():
            response = 'Ok, staller'
            await message.channel.send(response)

        elif 'git gud' in message.content:
            response = "`git: 'gud' is not a git command. See 'git --help'.`"
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

        elif message.content.startswith('!joke'):
            jokeStr = ""
            jokeJson = requests.get('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit').json()
            jokeJson = json.dumps(jokeJson)
            jokeJson = json.loads(jokeJson)

            if jokeJson['type'] == 'twopart':
                jokeStr += jokeJson['setup'] + "\n" + jokeJson['delivery'] + '\n'
            else:
                jokeStr += jokeJson['joke'] + "\n"
            await message.channel.send(jokeStr)

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

        elif message.content.startswith('!'):
            await message.channel.send("Unknown command. `!help` for commands.")


# Donations function
def donationStatsHandling():
    playerData = requests.get(clashApiUrl + urllib.parse.quote_plus(clantag) + '/members', headers = head).json()
    playerDataCD2 = requests.get(clashApiUrl + urllib.parse.quote_plus(clantag2) + '/members', headers = head).json()
    playerData['items'].extend(playerDataCD2['items'])

    # Currently all Alt accounts need to be added in manually
    #                 money        jabu          hurty          jabu
    altAccounts = {'#98VCGYCQ': '#U2Y9U82Q', '#2CG98CCCR' : '#U2Y9U82Q',\
    #   homme         nige         ethan2         ethan
     '#28880LJQ': '#28ULJVPP', '#2U2LP2GCG' : '#2JL80PJQC',\
    #   ethan3        ethan        ethan4         ethan
     '#C022UYPV': '#2JL80PJQC', '#LUPJ8Q8U8': '#2JL80PJQC'}

    donationString = '**Donations:**\n'
    donationDict = {}

    for item in playerData['items']:
        # read json data
        account = item['tag']
        # var for keeping player tags
        if account in altAccounts:
        # if the current tag in json data is found in the altAccounts dict
            primaryAccount = altAccounts[account]
            # Set the primary account to whatever the key is for the current account in the altAccounts dict
        else:
            # the account must not be found in the altAccounts dict
            primaryAccount = account
            # set the primary account to whatever the current tag is on

        if primaryAccount in donationDict:
        # if the primary account is in donationDict
            donationInfo = donationDict[primaryAccount]
            # set donationInfo to the data inside the donationDict primaryAccount (will be donations, and player name)
        else:
        # if the primaryAccount is not in donationDict
            donationInfo = [0, item['name']]
            # set the donation info to 0 donated, and the name of the player
        donationInfo[0] += item["donations"]
        # add the donations of the current account onto the donationInfo array
        donationDict[primaryAccount] = donationInfo
        # update the dict with the new donationInfo

    for i in donationDict:
        donationString += (donationDict[i][1])
        if i in altAccounts.values():
            donationString += (" *(Alt account(s) included)*")
        donationString += (": " + str(donationDict[i][0]) + "\n")

    print(donationDict)

    return donationString

bot.run(TOKEN)
