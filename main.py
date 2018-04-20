import tweepy

auth = tweepy.OAuthHandler('e3Qzanw0bnvTbunxOLr6GM2vi', 'IrBFKeNwfup4SRJDRtxwKsHJMRg5sppk6GD85GnWEKQ6b2Vfnk')
auth.set_access_token('1974502530-UIWm0t1pIzQMbmYgacEbrAf3TYKe1iMKn8op5hJ', 'KSCFR1kdXeESS4GrOfC37obNplr2wLRbmmhcBBgP69rnu')

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet
    break
