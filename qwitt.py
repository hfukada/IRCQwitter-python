# twitter things
from twitter import *
import json

import irc.client

# system imports
import time, sys

class Qwitter(irc.client.SimpleIRCClient):

  def __init__(self, configFile="config.json"):
    super(Qwitter, self).__init__()

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

    #for i in ["disconnect", "join", "kick", "mode","namreply", "nick", "part", "quit"]:
    #  self.connection.add_global_handler(i, getattr(self, "_on_" + i), -20)
    configs.print_configs(1)

  def _connect_checker(self):
    if not self.connection.is_connected():
      self.connection.execute_delayed(self.reconnectInterval, self._connect_checker)
      self.jump_server()

  def _connect(self):
    try:
      self.connect(self.server, self.port, self.nickname, ircname=self.realname)
    except irc.client.ServerConnectionError as e:
      print(e.value)

  def _on_disconnect(self, c, e):
    self.connection.execute_delayed(self.reconnectionInterval, self._connected_checker)

  def on_ctcp(self, c, e):
    """Default handler for ctcp events.

      Replies to VERSION and PING requests and relays DCC requests
      to the on_dccchat method.
    """
    nick = e.source.nick
    if e.arguments[0] == "VERSION":
      c.ctcp_reply(nick, "VERSION " + self.get_version())
    elif e.arguments[0] == "PING":
      if len(e.arguments) > 1:
        c.ctcp_reply(nick, "PING " + e.arguments[1])
    elif e.arguments[0] == "DCC" and e.arguments[1].split(" ", 1)[0] == "CHAT":
      self.on_dccchat(c, e)

  def start(self):
    self._connect()
    super(Qwitter,self).start()

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

if __name__ == '__main__':
  q = Qwitter("config.json")
  q.start()
