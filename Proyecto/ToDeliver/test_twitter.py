import twitter

if __name__ == '__main__':
    consumer_key = "CjuZ88saPFcFFlHSYGJrJQ"
    consumer_secret = "JCGyXY7ZJ5JdrNwYVnBqKaB9X0FA2ZVtq8gTsN2NT4"
    access_token = "185956451-EgLG7dqJ7L46glKg1RAxAner0z4VwK6bTmbvitqH"
    access_token_secret = "iO39CV1oLzxR3FgYHmKA1Ozexd0u7FgWvzFO41nhcLoIj"
    encoding = None
    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                      access_token_key=access_token, access_token_secret=access_token_secret,
                      input_encoding=encoding)
    #print api.VerifyCredentials()
    statuses = api.GetSearch("seat toledo")
    for status in statuses:
        print status
        #print "@%s"%status.user.screen_name, status.text
