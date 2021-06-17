import re, os, yaml

class ServerPartition(object):
   #__slots__ = ("name", "wait", "general", "announce")
   def __init__(self, name, wait, general, announce, **kwargs):
      self.__dict__.update(kwargs)
      self.name = name
      self.wait = wait
      self.general = general
      self.announce = announce

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
with open("config.yml") as f:
   data = yaml.load(f, Loader=yaml.FullLoader)
__bro_options = {"role_select": data["bro_role_select_id"]}
__sis_options = {"role_select": data["sis_role_select_id"]}
TEST_MODE = False; ENV = "PROD"; MSA = data["msa"]
BROTHERS = ServerPartition("Brother", data["bro_wait_id"],
                  data["bro_general_id"], data["bro_announce_id"],
                  **__bro_options)
SISTERS = ServerPartition("Sister", data["sis_wait_id"],
                 data["sis_general_id"], data["sis_announce_id"],
                 **__sis_options)
EMAIL = data["email"]
APP_PASS = data["app_pass"]
BOT = data["bot_pass"]
SP = ""
DB_SECRET = re.sub(r"\\n", '\n', "")
ENCRYPT_KEY = re.sub(r"\\n", '\n', "")
DB_PATH = "database/database.db"
VERIFY_ID = data["verify_id"]
SERVER_ID = data["server_id"]
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
'''
