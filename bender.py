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
devs = [143430791651655680, 390512772829544448, 478907955937411072]

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

        # give assistance (very un-bender-like)
        elif message.content == '!help':
            response = '`!donations`: List donations \n`!restart`: Restart bot (if it is misbehaving)'
            await message.channel.send(response)

        # explain self
        elif message.content == '!hi' or message.content == '!bot':
            response = 'I am Bender. Please insert girder.'
            await message.channel.send(response)

        # call out stallers
        elif 'not stall' in message.content or "i didn't stall" in message.content.lower() or 'i didnt stall' in message.content.lower():
            response = 'Ok, staller'
            await message.channel.send(response)

        # call out bad syntax
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

        # do as bender does best
        elif '!insult ' in message.content:
            person = message.content
            person = person.replace("!insult ", "")
            # do not insult self.
            if 'bender' in person.lower() or 'bot' in person.lower():
                person = "Bite my shiny metal ass."
                print("Someone tried to insult bot, but failed :-)")
            else:
                print("Insulted " + person)
                person += (' bad')
            await message.channel.send(person)

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

        # tell a joke
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
            print("Told joke")

        # API request (developer use only)
        elif message.content.startswith('!get') and message.author.id in devs:
            dataResponse = requests.get(clashApiUrl + urllib.parse.quote_plus(clantag), headers = head)
            jsonResponse = dataResponse.json()
            print(jsonResponse)

        elif message.content.startswith('!restart'):
            await message.channel.send("Restarting...")
            process.exit(1);

        # Donations
        elif message.content.startswith('!donations'):
            donations = donationStatsHandling()
            await message.channel.send(donations)
            print("Listed Donations")

        # Bender couldn't be bothered.
        elif message.content.startswith('! '):
            await message.channel.send("Unknown command. `!help` for commands.")

# Donations function
def donationStatsHandling():
    # Get data from API
    playerData = requests.get(clashApiUrl + urllib.parse.quote_plus(clantag) + '/members', headers = head).json()
    playerDataCD2 = requests.get(clashApiUrl + urllib.parse.quote_plus(clantag2) + '/members', headers = head).json()
    playerData['items'].extend(playerDataCD2['items'])

    # Currently all Alt accounts need to be added in manually
    #                 money        jabu          hurty          jabu
    altAccounts = {'#98VCGYCQ': '#U2Y9U82Q', '#2CG98CCCR' : '#U2Y9U82Q',\
    #   homme         nige         ethan2         ethan
     '#28880LJQ': '#28ULJVPP', '#2U2LP2GCG' : '#2JL80PJQC',\
    #   ethan3        ethan        ethan4         ethan
     '#C022UYPV': '#2JL80PJQC', '#LUPJ8Q8U8': '#2JL80PJQC',\
    #  cliff2       cliff         connor       cliff
     '#PLRUGG': '#29G2LJCU8', '#290RLQ2RJ': '#29G2LJCU8',\
    #   olivia        cliff          bot          cliff
     '#98YV29P99': '#29G2LJCU8', '#Q28PCL9PU': '#29G2LJCU8',\
    #   chinook        rain          wild2         wild
     '#Q28UJGYJ8': '#LYLP29U8R', '#Y09QGJRCQ': '#20PQ92V9J',\
    #   vampkon     vampwolf      vampmuis      vampwolf
     '#LUQJRRJ2Q': '#Q8C9L28L', '#LV92QVVYP': '#Q8C9L28L',\
    #  vampmeeuw     vampwolf      popcornv3      popcorn
     '#LUL8UPYYU' : '#Q8C9L28L', '#LPQPVGVGU': '#9PL80RPQR',\
    #   rushsam         sam          brosam         sam
     '#QYG8LRP20' : '#PVYCPL0Y2', '#LUVLC9QGP': '#PVYCPL0Y2',\
    #  darferino       darfo       gigadarf        darfo
     '#LY90RVV0U': '#L2URG8QCY', '#Q2Q9RG00R': '#L2URG8QCY',\
    #   tictac2      tictac      jeremysuf       jeremy
     '#QL8GPUGV0': '#VLQULJ8V', '#LGLRV0Y09': '#PRU8L9YCR',\
    #   mojie         moojie       smoljie        moojie
     '#YG8JPL98V': '#2GCVUPYUC', '#Q09LVGPQL': '#YG8JPL98V',\
    #   delph         nige          alan          nige
     '#2Y0LC00UY': '#28ULJVPP', '#L82CCUGV0': '#28ULJVPP'}

    donationString = '**Donations:**\n'
    donationDict = {}

    # Check if given player is in the list, if it's an alt, add it to main account instead of separately displaying
    for item in playerData['items']:
        account = item['tag']
        if account in altAccounts:
            primaryAccount = altAccounts[account]
        else:
            primaryAccount = account
        if primaryAccount in donationDict:
            donationInfo = donationDict[primaryAccount]
        else:
            donationInfo = [0, item['name']]
        donationInfo[0] += item["donations"]
        donationDict[primaryAccount] = donationInfo

    # Assemble string
    for i in donationDict:
        donationString += (donationDict[i][1])
        if i in altAccounts.values():
            donationString += (" **(Alts)**")
        donationString += (": " + str(donationDict[i][0]) + "\n")

    return donationString

bot.run(TOKEN)
