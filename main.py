import tweepy

auth = tweepy.OAuthHandler('e3Qzanw0bnvTbunxOLr6GM2vi', 'IrBFKeNwfup4SRJDRtxwKsHJMRg5sppk6GD85GnWEKQ6b2Vfnk')
api = tweepy.API(auth)
auth.set_access_token('1974502530-UIWm0t1pIzQMbmYgacEbrAf3TYKe1iMKn8op5hJ', 'KSCFR1kdXeESS4GrOfC37obNplr2wLRbmmhcBBgP69rnu')

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=[])

