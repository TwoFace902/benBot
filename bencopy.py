import discord
import json
import signal
import sys
from datetime import date
from random import *

file = "wordle.json"
client = discord.Client()
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
        await message.channel.send('just type \'ben [your question here]\' for a magical experience')
        await message.channel.send('in wordle-enthusiasts: \'ben stats [day]\' for basic info, ben is too stupid to do anything else rn')
        return
    if(message.channel.name == [your channel here]):
        bigboy = str(message.author.id)

        if message.content.startswith('Wordle '):
            info = (message.content.partition('/6')[0]).partition(' ')[2].split(' ')
            if bigboy in userDick:
                userDick[bigboy][info[0]] = int(info[1])
            else:
                userDick[bigboy] = {info[0]: int(info[1])}
            return
        if message.content.lower().startswith('ben stats '):
            thatday = message.content.split(' ')[2]
            await displayWordle(message,thatday,bigboy)            
    else:
        if message.content.lower().startswith('ben'):
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

async def displayWordle(message,day, author):
    global userDick
    if author not in userDick:
        await message.channel.send('you didnt do it retard')
        return
    if day in userDick[author]:
        await message.channel.send(message.author.name + '\'s Day ' + day + ' guesses: ' + str(userDick[author][day]))
        return
    else:
        await message.channel.send('you didnt do it retard')
        return

signal.signal(signal.SIGINT, signal_handler)
client.run([your bot id here])