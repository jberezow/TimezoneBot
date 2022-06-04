import json
import re
import random
from dataclasses import dataclass
import pytz


@dataclass
class Message:
    def __init__(self, content, author):
        self.content = content
        self.author = author

timezones = []

# List of relevant timezones
with open('timezones.json') as file:
    TIMEZONES = json.load(file)
with open('longTimezones.json') as file:
    LONG_TIMEZONES = json.load(file)

# Get Discord users from text file
with open('users.json', 'r') as file:
    USERTIMES = json.load(file)

# Get Discord users from text file
with open('TimezoneBot/users.json', 'r') as file:
    USERTIMES = json.load(file)

def dst_modifier(datetime_a, datetime_b, tz_a, tz_b):
    return 1

def get_user_timezone(user):
    time_code = USERTIMES[user]
    return time_code

def convert_timezone(a, b, time):
    if a == b:
        return time
    else:
        at = TIMEZONES[a]
        bt = TIMEZONES[b]
        difference = at - bt # Subtract this amount
        hour, minute = time.split(":")
        hour = int(hour)
        new_hour = hour - difference
        if new_hour < 0:
            new_hour = 24 + new_hour
        elif new_hour > 24:
            new_hour = new_hour % 24
    
    return str(new_hour) + ":" + minute

def on_message(message):

    message_times = re.findall("\d*:\d*", message.content)

    if message_times:
        for time in message_times:
            timezone = get_user_timezone(message.author)
            response = f"""
                {message.author} indicated a time: {time} {timezone}\nHere is the time in other timezones:\n----------------------------------------
            """
            for conversion in TIMEZONES.keys():
                converted = convert_timezone(timezone,conversion,time)
                response += f"\n {conversion}: {converted}"
            print(response) # message.channel.send(response)

def main():
    print("Timezoney the timezone bot is live")
    while True:
        author_int = random.randint(0,len(list(USERTIMES))-1)
        author = list(USERTIMES)[author_int]
        content = input(f"{author}, please enter a Discord message:\n")
        message = Message(content, author)
        on_message(message)
    
if __name__ == '__main__':
    main()
