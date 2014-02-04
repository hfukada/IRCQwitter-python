import twitter
import twitter_secrets
import irc

class qwitter:

  def __init__ ( self, secrets ):
    self.api = twitter.Api(consumer_key=secrets.consumer_key, consumer_secret=secrets.consumer_secret, access_token_key=secrets.access_token_key, access_token_secret=secrets.access_token_secrets)
    self.irc

  def runBot():





