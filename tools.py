import asyncio
import re, os, time, yaml, smtplib
import mysql.connector
from random import randint
from email.message import EmailMessage
from key import db_pass, email_pass
from config import *
login = db_pass()
app_pass = email_pass()

#If email treated as spam:
 #https://support.google.com/mail/contact/bulk_send_new?rd=1
#Print Emojis Safely
 #print(u'\U0001f604'.encode('unicode-escape'))
 #print('\N{grinning face with smiling eyes}')
#Make way to update #role-selection

BEN_10 = ["Heatblast", "Wildmutt", "Diamondhead", "XLR8", "Grey Matter",
          "Four Arms", "Stinkfly", "Ripjaws", "Upgrade", "Ghostfreak",
          "Cannonbolt", "Ditto", "Way Big", "Upchuck",
          "Wildvine", "Alien X", "Echo Echo", "Brainstorm", "Swampfire",
          "Humongousaur", "Jetray", "Big Chill", "Chromastone", "Goop",
          "Spidermonkey", "Rath", "Nanomech"]
SIKE = {'@':'a', '!': 'i', '1': 'i', '5': 's',
        '3': 'e', '0': 'o', 'l': 'i'}
CURSES = ["retard", "fuck", "shit", "ass",
          "heii", "pussy", "fucker",
          "dick", "nigger", "bitch", "nigg",
          "damn", "prick", "nigga", "hoe",
          "siut", "whore", "cunt", "dickhead"]
ROLE_EMOJIS = {"\U0001f9d5": 750931950964965506,
               "\N{BABY}": 750922989972750337,
               "\N{GIRL}": 750923173956026438,
               "\N{WOMAN}": 750923497101983795,
               "\N{OLDER WOMAN}": 750923619634249740,
               "\N{STRAIGHT RULER}": 756328774764593173,
               "\N{DESKTOP COMPUTER}": 756329639588397197,
               "\N{ATOM SYMBOL}": 756334778881540137,
               "\N{TEST TUBE}": 756335021933068288,
               "\N{OPEN BOOK}": 762052942302937111,
               "\U0001f4f6": 783048947291258920,
               "\U0001f9a0": 783049863243104296,
               "\U0001f9be": 783050320552001587,
               "\U0001f3d7": 783050450462703616,
               "\U0001f4af": 778401907713638460,
               "\U0001f310": 805947673043664919}

def edit_file(file, value):
    with open(file, 'r+') as f:
        lines = f.readlines()
        f.seek(0); found = False
        for line in lines:
            line = line.strip('\n')
            if str(line).lower() != str(value).lower():
                f.write(line + '\n')
            else:
                found = True
        f.truncate()
        return found

def send_email(addr: str, test=False) -> str: # Return 4-digit verification code string
    sCode = f"{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}"
    if not test:
        msg = EmailMessage()
        msg.set_content(f"\
    <html><body><b>Your verification code to join the chat is below:<br><br>\
    <h2>{sCode}</h2></b>Please copy & paste this code in the \
    <i><u>#verify</u></i> text channel of your NJIT MSA Discord. \
    This code will expire in 15 minutes.</body></html>", subtype="html")
        msg["Subject"] = "Verification Code for NJIT MSA Discord"
        msg["From"] = "noreply.njitmsa@gmail.com"
        msg["To"] = addr
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login("noreply.njitmsa@gmail.com", APP_PASS)
                s.send_message(msg)
    else:
        print(sCode)
    return sCode

def curse_check(msg: str) -> bool:
    msg = msg.replace('l', 'i')
    wordCheck = ''
    for i in range(len(msg)):
        char = msg[i]
        if char in SIKE:
            char = SIKE[char]
        wordCheck += char
        wordCheck = wordCheck.strip(' ')
        if wordCheck in CURSES:
            
            try:
                if msg[i+1] != char or msg[i+1] != ' ':
                    wordCheck = ''
                    continue
            except IndexError:
                pass
            return True
    for curse in CURSES:
        if re.search(fr"\b{curse}\b", msg):
            return True
    return False

def get_name(addr: str) -> str: # Return full name string based on email
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=login,
            database="contacts")
        mycursor = mydb.cursor()
        ucid = re.sub(r"@njit\.edu", '', addr)
        sql = f"SELECT full_name FROM links WHERE ucid='{ucid}'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        if len(result) != 0:
            return str(result[0][0])
    except mysql.connector.Error as err:
        print(f"Error: Could not connect:\n\tDetails: {err}")

def check_gender(user):
    roles = user.roles
    for role in roles:
        if role.name == "Brother" or role.name == "Sister":
            return role.name

def check_admin(msg):
    roles = msg.author.roles
    for role in roles:
        if role.name == "Admin" or "Shura" in role.name:
            return True
    return False

def ben_10(choice=''):
    choice = choice.strip(' '); alien_form = ''
    if choice == '':
        idx = randint(0,28)
        alien_form = BEN_10[idx]
    else:
        for alien in BEN_10:
            if alien.lower() in choice.lower():
                got = randint(1,3)
                if got == 1:
                    alien_form = alien; break
                else:
                    ignore = BEN_10.index(alien)
                    idx = randint(0,26)
                    temp = BEN_10[:ignore] + BEN_10[ignore+1:]
                    alien_form = temp[idx]; break
        if alien_form == '':
            idx = randint(0,27)
            alien_form = BEN_10[idx]
    return alien_form

def get_sibling_role(member):
    roles = member.roles; ret = None
    for role in roles:
        if role.name == "Brothers Waiting Room":
            ret = ("Brother", role); break
        elif role.name == "Sisters Waiting Room":
            ret = ("Sister", role); break
    return ret

def get_sibling(sibling):
    if sibling == "Brother":
        return brothers
    else:
        return sisters

def listen_announce(msg):
    if msg.channel.id == brothers.announce:
        if "@everyone" in msg.content:
            return sisters.announce
    elif msg.channel.id == sisters.announce:
        if "@everyone" in msg.content:
            return brothers.announce
    else:
        False

def listen_role_reaction(raw_emoji):
    role_id = 0
    emoji = raw_emoji.name.encode('unicode-escape')
    emote = re.search(r".+?\\", str(emoji).strip("b'\\"))
    if emote and str(emoji).lower().count('u') > 1:
        emoji = ("\\" + emote.group().strip('\\')).encode()
    for role_emoji in ROLE_EMOJIS:
        if emoji == role_emoji.encode('unicode-escape'):
            return ROLE_EMOJIS[role_emoji]
    return False

def listen_verify(msg):
    if msg.channel.id == VERIFY_ID:
        if msg.content.startswith('/verify'):
            request = re.sub(r"/verify ", '', msg.content.lower())
            gender = re.search(r"(brothers?|sis(tas?|ters?))", request) or ''
            if gender:
                ucid = re.sub(fr"{gender.group()}", '', request).strip(' ')
                if gender.group()[0] == 'b':
                    gender = "Brother"
                else:
                    gender = "Sister"
                return ucid, gender
            return ('', '')

def listen_code(msg):
    if msg.channel.id == VERIFY_ID:
        return re.search(r"^\d\d\d\d$", msg.content)

def in_general(channel_id):
    if channel_id == brothers.general:
        return brothers
    elif channel_id == sisters.general:
        return sisters
    else:
        return False

async def mute_voice_members(voice_channel, mute=True):
    for member in voice_channel.members:
        await member.edit(mute=mute)

async def check_verify(record, msg, temp):
    while True:
        with open("verify.txt") as f:
            text = f.read()
            if not re.search(fr"{record}", text):
                break
        await asyncio.sleep(0)
    await msg.delete(); await temp.delete()
