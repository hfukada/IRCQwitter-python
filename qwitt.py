# twitter things
import twitter
import bot_config

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys



class Qwitter:

  def __init__ ( self, secrets ):
    self.api = twitter.Api(consumer_key=secrets.consumer_key, consumer_secret=secrets.consumer_secret, access_token_key=secrets.access_token_key, access_token_secret=secrets.access_token_secrets)
    self.secrets = secrets

  def runBot():
    run

class QwittFactory(protocol.ClientFactory):
  def __init__( self, channel ):

