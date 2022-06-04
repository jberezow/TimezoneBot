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

async def convert_from_pm(time):
    hour, minute = time.split(":")
    hour = int(hour)
    new_hour = hour + 12
    return str(new_hour) + ":" + minute

async def convert_to_pm(time):
    hour, minute = time.split(":")
    hour = int(hour)
    if hour < 12:
        return str(hour) + ":" + minute + "AM"
    elif hour == 12:
        return str(hour) + ":" + minute + "PM"
    else:
        new_hour = hour % 12
        return str(new_hour) + ":" + minute + "PM"

async def handle_pm(time):
    raw_time_match = re.match("\d*:\d*", time)
    raw_time = time[raw_time_match.start():raw_time_match.end()]
    pm_match = re.findall("(pm)|(PM)",time)
    if len(pm_match) == 0:
        return raw_time
    else:
        new_time = await convert_from_pm(raw_time)
        return new_time

@tz.event
async def on_message(message):

    # Don't reply to timezone bot
    if message.author == tz.user:
        return

    message_times = re.findall(r"^\d{1,2}:\d{1,2}$|^\d{1,2}:\d{1,2} pm$|^\d{1,2}:\d{1,2} PM$|^\d{1,2}:\d{1,2}pm$|^\d{1,2}:\d{1,2}PM$", message.content)

    if message_times:
        for time in message_times:
            timezone = await get_user_timezone(message.author.name)
            time = await handle_pm(time)
            time_pm = await convert_to_pm(time)
            response = [f"```{message.author.name} indicated a time: **{time} {timezone} ({time_pm})**\n\nHere is the time in other timezones:\n----------------------------------------------"]
            for conversion in TIMEZONES.keys():
                converted = await convert_timezone(timezone,conversion,time)
                target_tz = LONG_TIMEZONES[conversion]
                dif = 25 - len(target_tz)
                converted_pm = await convert_to_pm(converted)
                response.append(f"\n{(target_tz+':'+''.join([' ' for _ in range(dif)]))}{converted :>10}{converted_pm :>10}")
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