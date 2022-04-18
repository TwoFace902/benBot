import discord
import json
import signal
import sys
from datetime import date
from random import *

benfollowups = [' ' , ',' , '!' , '?' , '.', ':']
file = "wordle.json"
intents = discord.Intents().all()
client = discord.Client(intents=intents)
userDick = dict({})


@client.event
async def on_ready():
    global userDick
    with open(file,'r') as f:
        userDick = json.load(f)
    await client.change_presence(activity=discord.Game("\'ben cmd\' for help"))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global userDick
    if message.author == client.user:
        return
    if(message.content.lower() == 'ben cmd'):
        await message.channel.send('---[BASIC INFO]---\n```just type \'ben [your question here]\' for a magical experience```\n---[IN WORDLE-ENTHUSIASTS ONLY]---\n```\'ben mystats [day]\' for day\'s result\n\'ben overall @[the dork u want to alert to your shenanigans]\' for overall info\n\'ben daywinner [day]\' for the day\'s winners```')
        return
    if(message.channel.name == 'wordle-enthusiasts'):
        bigboy = str(message.author.id)
        if message.content.startswith('Wordle '):
            info = (message.content.partition('/6')[0]).partition(' ')[2].split(' ')
            if info[1] == 'X':
                info[1] = -1
            if bigboy in userDick:
                userDick[bigboy][info[0]] = int(info[1])
            else:
                userDick[bigboy] = {info[0]: int(info[1])}
            return
        if message.content.lower().startswith('ben mystats '):
            thatday = message.content.split(' ')[2]
            if(thatday.isdecimal() and int(thatday) >= 0):
                await displayDay(message,thatday,bigboy)
            else:
                await message.channel.send('that\'s not a day moron')
            return
        if message.content.lower().startswith('ben daywinner '):
            thatday = message.content.split(' ')[2]
            if(thatday.isdecimal() and int(thatday) >= 0):
                await displayWinner(message,thatday)
            else:
                await message.channel.send('that\'s not a day moron')
        if message.content.lower().startswith('ben overall'):
            for boy in message.mentions:
                await displayOverall(message, str(boy.id))
    else:
        if message.content.lower().startswith('ben') and (len(message.content) < 4 or message.content[3] in benfollowups):
            benquotes = ['Yes','No','Ho ho ho','eugh']
            benlogic = randint(0,len(benquotes)-1)
            await message.channel.send(benquotes[benlogic])
            
def signal_handler(signal, frame):
    writeRoutine()
    print('Death approaches')
    sys.exit(0)

def writeRoutine():
    global userDick
    f = open(file, 'w')
    json.dump(userDick,f)
    f.close()

async def scraping():
    async for message2 in message.channel.history(limit=None):
        bigboy = str(message2.author.id)
        if message2.content.startswith('Wordle '):
            print(message2.content)
            info = (message2.content.partition('/6')[0]).partition(' ')[2].split(' ')
            if info[1] == 'X':
                info[1] = -1
            if bigboy in userDick:
                userDick[bigboy][info[0]] = int(info[1])
            else:
                userDick[bigboy] = {info[0]: int(info[1])}
    print('Done!')

async def displayDay(message,day,author):
    global userDick
    if author not in userDick:
        await message.channel.send('you didnt do it retard')
        return
    if day in userDick[author]:
        if(userDick[author][day] == -1):
            res = 'Failed'
        else:
            res = str(userDick[author][day]) + ' guesses'
        await message.channel.send(message.author.nick + '\'s Day ' + day + ' result: ' + res)
        return
    else:
        await message.channel.send('you didnt do it retard')
        return

async def displayWinner(message,day):
    global userDick
    guild = message.guild
    winners = 0
    outStr = 'The winner(s) for Wordle ' + day + ': '
    winnerList = []
    guess = 7
    for men in userDick:
        if(day in userDick[men]):
            if(userDick[men][day] < guess and userDick[men][day] > 0):
                winnerList.clear()
                winnerList.append(men)
                guess = userDick[men][day]
            elif(userDick[men][day] == guess):
                winnerList.append(men)
    for men in winnerList:
        winners += 1
        user = guild.get_member(int(men))
        outStr += user.nick + ', '
    #outStr = outStr[:,-2]
    outStr += 'with ' + str(guess) + ' guesses.'
    if(winners == 0):
        outStr = 'Nobody won Wordle ' + day
    await message.channel.send(outStr)

async def displayOverall(message,bigboy):
    global userDick
    if bigboy not in userDick:
        await message.channel.send('No games played for this user.')
        return
    prevDay = -1
    streakC = 0
    streakT = 0
    wTot = len(userDick[bigboy].keys())
    wCnt = 0.0
    for key in sorted(userDick[bigboy]):
        if(prevDay != -1 and (int(key) - prevDay > 1)):
            if(streakC > streakT):
                streakT = streakC
            streakC = 0
        if userDick[bigboy][key] != -1:
            wCnt += 1
            streakC += 1
        else:
            if(streakC > streakT):
                streakT = streakC
            streakC = 0
        prevDay = int(key)
    if(streakC > streakT):
        streakT = streakC
    await message.channel.send('Total games played: ' + str(wTot) + '\nWinrate: ' + '{pct:.2f}'.format(pct = (wCnt * 100)/wTot) + '%\nCurrent streak: ' + str(streakC) + '\nLongest streak: ' + str(streakT))

signal.signal(signal.SIGINT, signal_handler)
client.run('you're token heer')