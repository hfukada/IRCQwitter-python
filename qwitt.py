# twitter things
import twitter
import json

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys

class Qwitter(irc.IRCClient):

  def connectionMade(self):
    self.nickname = self.factory.nickname
    self.realname = self.factory.realname
    self.username = self.factory.username
    self.owner = self.factory.owner

    self.api = self.factory.api
    irc.IRCClient.connectionMade(self)
    print "connection has been made"

  def connectionLost(self, reason):
    print "Connection has been lost: " + reason

  def signedOn(self):
    print "Signed on"
    self.join(self.factory.channel)

  def joined(self, channel):
    print "Joined channel: " + channel

  def privmsg(self, user, channel, msg):
    print "Got private message: " + msg + " from: " + channel + ":user"+user


class QwittFactory(protocol.ClientFactory):

  def __init__(self, configFile="config.json"):
    # load configs from external file
    configs = bot_configs(config=configFile)

    self.nickname = configs.nick
    self.username = configs.userName
    self.realname = configs.realName
    self.owner = configs.owner

    self.server = configs.server
    self.port = configs.port
    self.channel = configs.channel

    # Twitter configs for posting
    # self.consumer_key = configs.consumer_key
    # self.consumer_secret = configs.consumer_secret
    # self.access_token_key = configs.access_token_key
    # self.access_token_secret = configs.access_token_secret

    # API for twitter talking
    self.api = twitter.Api(consumer_key=configs.consumer_key, consumer_secret=configs.consumer_secret, access_token_key=configs.access_token_key, access_token_secret=configs.access_token_configs)

  def buildProtocol(self, addr):
    p = Qwitter()
    p.factory = self
    return p

  def clientConnectionLost(self, connector, reason):
    # if we DC then we connect back
    print "Reconnecting..."
    connector.connect()

  def clientConnectionFailed(self, connector, reason):
    # Failed
    print "connection failed: " + reason

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

  def print_configs(self, debug = 0):
    if debug == 0:
      return
    print "Consumer key " + self.consumer_key
    print "Consumer Secret " + self.consumer_secret
    print "Access Taken Key " + self.access_token_key
    print "Access Token Secret " + self.access_token_secret

    print "Owner " + self.owner
    print "Nick " + self.nick
    print "User " + self.userName
    print "Real " + self.realName
    print "Server " + self.server
    print "Port " + str(self.port)

if __name__ == '__main__':
  q = QwittFactory("config.json")
  reactor.connectTCP(q.server, q.port, q)
  q.run()
