import re, os

class ServerPartition(object):
   #__slots__ = ("name", "wait", "general", "announce")
   def __init__(self, name, wait, general, announce, **kwargs):
      self.__dict__.update(kwargs)
      self.name = name
      self.wait = wait
      self.general = general
      self.announce = announce

__bro_options = {"role_select": 792531850740498482}
__sis_options = {"role_select": 792531967832227841}

# Update the role-selection listener
def update_role_select():
   with open("role_selection.txt", encoding="utf-8") as f:
      lines = f.readlines()
      for line in lines:
         extra, emote, role = line.split(' ')
         if extra == 0 and emote not in ROLE_EMOJIS:
            ROLE_EMOJIS[emote] = int(role)
         elif extra != 0 and \
              emote not in SPLIT_ROLES_EMOJIS[BROTHERS.role_select] or \
              emote not in SPLIT_ROLES_EMOJIS[SISTERS.role_select]:
            SPLIT_ROLES_EMOJIS[BROTHERS.role_select][emote] = int(role)
            SPLIT_ROLES_EMOJIS[SISTERS.role_select][emote] = int(extra)


# Set all global variables
BROTHERS = ServerPartition("Brother", 748745649746477086,
                  631090067963772931, 687402472586870849,
                  **__bro_options)
SISTERS = ServerPartition("Sister", 748761869480624158,
                 748762901531066458, 748764105686384650,
                 **__sis_options)
TEST_MODE = False; ENV = "DEV"; MSA = "NJIT"
EMAIL = ""
APP_PASS = ""
BOT = ""
SP = ""
DB_SECRET = re.sub(r"\\n", '\n', "")
ENCRYPT_KEY = re.sub(r"\\n", '\n', "")
DB_PATH = "database/database.db"
VERIFY_ID = 688625250832744449
SERVER_ID = 630888887375364126
ROLE_EMOJIS = {}
SPLIT_ROLES_EMOJIS = {BROTHERS.role_select: {},
                      SISTERS.role_select: {}}
DEVS = [233691753922691072]
#os.chdir(CWD) # Return to original directory
update_role_select() # Update the role-selection listener upon startup

'''
Notes:
- Create Brother/Sister roles role
- Create #verify chat
- Enable Developer Mode
  Copy ID's:
  - Right click on Server Name
  - Right click on #verify chat
  - Right click on #general chat
- Make @everyone role only able to talk in #verify chat

Make MSA-Bot ready for website automatic setup
Make website that configures and download zip file of custom MSA bot
'''
