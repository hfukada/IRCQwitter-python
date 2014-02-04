import json

class twitter_secrets:
  __init__(self, config="config.json"):
    config = open(config)
    config = json.loads(configInfoJson)

    # twitter keys and configs
    self.consumer_key = config['consumer_key']
    self.consumer_secret = config['consumer_secret']
    self.access_token_key= config['access_token_key']
    self.access_token_secret = config['access_token_secret']

    # server/IRC specific configs
    self.owner = config['owner']
    self.nick = config['nick']
    self.userName = config['username']
    self.realName = config['realname']
    self.server = config['server']
    self.port = config['port']

