# twitter things
from twitter import *
import json

import irc.bot

# system imports
import time, sys

class Qwitter(irc.bot.SingleServerIRCBot):

  def __init__(self, configFile="config.json"):
    configs = bot_configs(config=configFile)

    self.nickname = configs.nick
    self.username = configs.userName
    self.realname = configs.realName
    self.channel = configs.channel
    self.owner = configs.owner

    self.server = configs.server
    self.port = configs.port
    self.channel = configs.channel
    self.reconnectInterval = configs.reconnectInterval

    # Twitter configs for posting
    # self.consumer_key = configs.consumer_key
    # self.consumer_secret = configs.consumer_secret
    # self.access_token_key = configs.access_token_key
    # self.access_token_secret = configs.access_token_secret

    # API for twitter talking
    self.t = Twitter(auth=OAuth(configs.access_token_key, configs.access_token_secret, configs.consumer_key, configs.consumer_secret) )
    irc.bot.SingleServerIRCBot.__init__(self, [(self.server, self.port)], self.nickname, self.realname, reconnection_interval=self.reconnectInterval)
    configs.print_configs(1)
    self.blacklist = configs.blacklist
    self.userquotes = {}
    self.commands = ["join", "say", "quoth"]
    self.allhist = []
    self.reset = True

  def on_welcome(self, connection, event):
    connection.join(self.channel)

  def on_privmsg(self, connection, event):
    if event.source.nick == self.owner:
      self.do_command(connection, event)

  def on_pubmsg(self, connection, event):
    if not self.inBlacklist(event.arguments[0]):
      self.allhist.append("<" + event.source.nick + "> " + event.arguments[0])
      if len(self.allhist) > 2 and self.carrotCheck():
        self.sendTweet(self.allhist[-3])
        connection.privmsg(event.target, "Posting: " + self.allhist[-3] + " to @QuothTheDong")
        self.allhist = []

    if self.recordLine(event.arguments[0]):
      """ Add the line to the user queue if it exists """
      self.reset = True
      if event.source.nick in self.userquotes:
        self.userquotes[event.source.nick].append(event.arguments[0])
      else:
        self.userquotes[event.source.nick] = [event.arguments[0]]
    else:
      self.do_command(connection, event)

  def do_command(self, connection, event):

    cmd = event.arguments[0].split()[0]
    args = list(filter(None, event.arguments[0].split(' ')[1:]))

    if cmd[0] != '!':
      return

    if cmd == "!join" and event.source.nick == self.owner:
      connection.join(args[0])
    elif cmd == "!say" and event.source.nick == self.owner:
      connection.privmsg(args[0], ' '.join(args[1:]))
    elif cmd == "!print" and event.source.nick == self.owner:
      print(self.allhist)
      print(self.userquotes)
    elif cmd == "!clean" and event.source.nick == self.owner:
      for user in self.userquotes:
        if len(self.userquotes[user]) > 500:
          self.userquotes[user] = self.userquotes[user][-500:]
      connection.privmsg(self.owner, "Clean up the crap")
    elif cmd == "!quo" or cmd == "!quoth":
      if len(args) > 1:
        self.handleQuoth(args[0], connection, event, scrollback=args[1])
      else:
        self.handleQuoth(args[0], connection, event)
    elif cmd =="!qwittdesc":
      self.updateDescription(' '.join(args))
      connection.privmsg(event.target, "Updated description: https://twitter.com/QuothTheDong")

  def inBlacklist(self, line):
    for word in self.blacklist:
      if word in line:
        return True
    return False

  def recordLine(self, line):
    if line.count('^') > len(line)/2:
      return False
    else:
      return not self.inBlacklist(line)

  def carrotCheck(self):
    prevline = self.getTrimmedLine(self.allhist[-1])
    prev2line = self.getTrimmedLine(self.allhist[-2])
    if prevline.count('^') > len(prevline)/2 and prev2line[-1].count('^') > len(prev2line)/2 and self.reset:
      self.reset = False
      return True
    return False

  def getTrimmedLine(self, line):
    return line.split('> ')[1:]

  def handleQuoth(self, nick, connection, event, scrollback="1"):
    if scrollback.isdigit():
      scrollback = int(scrollback)
      if scrollback <= 0:
        connection.privmsg(event.source.nick, "I don't know the future for that person")
        return
    else:
      connection.privmsg(event.source.nick, "Enter a number you fool. Usage !quoth <nick> [scrollback]")
      return

    if nick in self.userquotes:
      if len(self.userquotes[nick]) >= scrollback:
        offset = len(self.userquotes[nick])
        self.sendTweet("<" + nick + "> " + self.userquotes[nick][offset-scrollback])
        connection.privmsg(event.source.nick, "Posting to @QuothTheDong: " + "<" + nick + "> " + self.userquotes[nick][offset-scrollback])
      else:
        connection.privmsg(event.source.nick, "History for %s does not exist that far"%(nick))
    else:
      connection.privmsg(event.source.nick, "Nick: %s does not exist"%(nick))

  def sendTweet(self, text):
    # print("Posting: %s"%(text))
    try:
      self.t.statuses.update(status=text)
    except Exception:
      pass


  def updateDescription(self, text):
    # print(text)
    try:
      self.t.account.update_profile(description=text)
    except Exception:
      pass


class bot_configs:
  def __init__(self, config="config.json"):
    configInfoJson = open(config)
    config = json.load(configInfoJson)

    # twitter keys and configs
    self.consumer_key = config['consumer_key']
    self.consumer_secret = config['consumer_secret']
    self.access_token_key= config['access_token_key']
    self.access_token_secret = config['access_token_secret']

    # server/IRC specific configs
    self.owner = config['owner']
    self.nick = config['nick']
    self.userName = config['userName']
    self.realName = config['realName']
    self.server = config['server']
    self.port = config['port']
    self.channel = config['mainChannel']
    self.reconnectInterval = config['reconnectInterval']
    self.blacklist = config['blacklist']

  def print_configs(self, debug = 1):
    if debug == 0:
      return
    print("Consumer key " + self.consumer_key)
    print("Consumer Secret " + self.consumer_secret)
    print("Access Taken Key " + self.access_token_key)
    print("Access Token Secret " + self.access_token_secret)

    print("Owner " + self.owner)
    print("Nick " + self.nick)
    print("User " + self.userName)
    print("Real " + self.realName)
    print("Server " + self.server)
    print("Port " + str(self.port))
    print("Channel " + self.channel)

if __name__ == '__main__':
  q = Qwitter("config.json")
  q.start()
