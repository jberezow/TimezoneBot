import discord
import asyncio
import re
import pytz
import json
from discord.ext import commands

# Get Discord Token
with open('token.txt', 'r') as file:
    TOKEN = file.read()

timezones = []

intents = discord.Intents.default()
intents.members = True
discord.MemberCacheFlags.all()
tz = commands.Bot("$", intents=intents)

# List of relevant timezones
with open('timezones.json') as file:
    TIMEZONES = json.load(file)
with open('longTimezones.json') as file:
    LONG_TIMEZONES = json.load(file)

# Get Discord users from text file
with open('users.json', 'r') as file:
    USERTIMES = json.load(file)

async def dst_modifier(datetime_a, datetime_b, tz_a, tz_b):
    return 1

async def get_user_timezone(user):
    time_code = USERTIMES[user]
    return time_code

async def convert_timezone(a, b, time):
    if a == b:
        return time
    else:
        at = TIMEZONES[a]
        bt = TIMEZONES[b]
        difference = at - bt # Subtract this amount
        hour, minute = time.split(":")
        hour = int(hour)
        new_hour = hour - difference
        new_hour = new_hour % 24
    
    return str(new_hour) + ":" + minute

@tz.event
async def on_message(message):

    # Don't reply to timezone bot
    if message.author == tz.user:
        return

    message_times = re.findall("\d*:\d*", message.content)

    if message_times:
        for time in message_times:
            timezone = await get_user_timezone(message.author.name)
            response = [f"```{message.author.name} indicated a time: **{time} {timezone}**\n\nHere is the time in other timezones:\n--------------------------------------"]
            for conversion in TIMEZONES.keys():
                converted = await convert_timezone(timezone,conversion,time)
                target_tz = LONG_TIMEZONES[conversion]
                dif = 25 - len(target_tz)
                print(dif)
                response.append(f"\n{(target_tz+':'+''.join([' ' for _ in range(dif)]))}{converted :>10}")
            response.append("```")
            response = "".join(response)
            await message.channel.send(response)

@tz.event
async def on_ready():
    print("{} is now online".format(tz.user.name))
    print("Client user id: {}".format(tz.user.id))

def main():
    print("Timezoney the timezone bot is live")
    tz.run(TOKEN)
    
if __name__ == '__main__':
    main()