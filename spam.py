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
            print ("Found pattern at index " + str(i-j))
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
    fail = [0]
 
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

if __name__ == "__main__":
    txt = "ABABDABACDABABCABAB"
    pat = "CABAB"
    KMPSearch(pat, txt)