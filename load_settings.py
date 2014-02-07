import json

class load_settings:
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

if __name__=='__main__':
  botConfigs = load_settings()
  botConfigs.print_configs( debug=1 )
