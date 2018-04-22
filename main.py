import tweepy
import time

# Python program for KMP Algorithm
def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)
    fail = computeFailArray(pat, M)
    j = 0 # index for pat[]
    i = 0 # index for txt[]

    while i < N:
        if pat[j] == txt[i]: # match -> periksa karakter selanjutnya
            i += 1
            j += 1
 
        if j == M: # Pattern ditemukan dalam teks
            return True
 
        # mismatch 
        elif i < N and pat[j] != txt[i]:
            if j != 0:# mismatch bukan pada karakter pertama -> geser pattern sejauh fail[j-1] - j karakter
                j = fail[j-1]
            else:# mismatch pada karakter pertama -> geser pattern sejauh 1 karakter
                i += 1
        
    return False

def computeFailArray(pat, patlen):
    k = 0
    j = 1
    fail = [0]*len(pat)
 
    while j < patlen:
        if pat[j] == pat[k]:
            k += 1
            fail[j] = k
            j += 1
        else:
            if k != 0:
                k = fail[k-1]
            else:
                fail.insert(j, 0)
                j += 1
    return fail



auth = tweepy.OAuthHandler('e3Qzanw0bnvTbunxOLr6GM2vi', 'IrBFKeNwfup4SRJDRtxwKsHJMRg5sppk6GD85GnWEKQ6b2Vfnk')
api = tweepy.API(auth)
auth.set_access_token('1974502530-UIWm0t1pIzQMbmYgacEbrAf3TYKe1iMKn8op5hJ', 'KSCFR1kdXeESS4GrOfC37obNplr2wLRbmmhcBBgP69rnu')

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        #print status.text.encode('ascii', 'ignore');
        time.sleep(1)
        print status.text.encode('ascii', 'ignore')
        print "+++++++++++++++++++++++++++++++++"
        if KMPSearch("indo", status.text.encode("ascii", "ignore")):
            print status.text
            print '======================='

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=["indo"])

