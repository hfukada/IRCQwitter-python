# twitter things
import twitter
import bot_configs

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

  def joined(self, channel):
    print "Joined channel: " + channel

  def privmsg(self, user, channel, msg):
    print "Got private message"


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
