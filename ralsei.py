# ----------------------------------
# Ralsei Base
# Created by Infinidoge
# ----------------------------------
# Ralsei discord bot, build to be a general use bot with the ability to dynamically add commands
# ----------------------------------

import discord
import asyncio
from utils.misc_utils import find_files
from utils.config import Client
from utils.permissions import Perms

client = discord.Client()
config = Client()
perms = Perms()
if perms.owner_id == "blank":
    print("[Ralsei/Warn] owner id not set, continuing to run bot but beware that some commands may be unusable")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# Define utility functions

async def pre_cmd(message):
    return message


async def exec_cmd(message):
    try:
        await cmd[message.content.replace(config.prefix, "").split(' ')[0]](client, message)
    except KeyError:
        await client.send_message(message.channel,
                                  "I'm sorry <@%s>, but i have no idea what you just asked me to do. Sorry!" %
                                  message.author.id)


async def post_cmd(message):
    if not client.is_closed:
        await client.delete_message(message)


# ------------------------


# Define command functions

# ------------------------
cmd = {}
for i in find_files(config.location + "cmds"):
    i = i.replace(".py", "")
    exec("from cmds.%s import %s" % (i, i), globals())
    cmd[i.replace("_cmd", "")] = eval(i)


@client.event
async def on_message(message):
    if message.content.startswith(config.prefix):
        await pre_cmd(message)

        if message.content.startswith("!disabled"):
            await asyncio.sleep(1)
            await client.send_message(message.channel, "That command is disabled, sorry!")
        else:
            await exec_cmd(message)

        await post_cmd(message)

if config.token is not "blank":
    client.run(config.token)
else:
    print("Config is blank, fill in a token!")
