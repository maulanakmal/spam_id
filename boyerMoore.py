def charIndex(ch):
    return ord(ch.lower()) - 97 # start from 'a'

def matchLen(S, i, j):
    # counts elements of the match of the substrings of S beginning at i and j. Returns count
    if i == j:
        return len(S) - i
    else:
        count = 0
        while i < len(S) and j < len(S) and S[i] == S[j]:
            count += 1
            i += 1
            j += 1
        return count

def preprocess(S):
    if len(S) == 0: # Base 0 : Handles case of empty string
        return []
    elif len(S) == 1: # Base 1 : Handles case of single-character string
        return [1]
    else: # recursive: more than one character
        res = [0 for x in S]
        res[0] = len(S)
        res[1] = matchLen(S, 0, 1)
        for i in range(2, 1+res[1]):
            res[i] = res[1] - i + 1
        l = 0
        r = 0
        for i in range(2 + res[1], len(S)):
            if i <= r:
                b = res[i - l]
                a = r - i + 1
                if b < a:
                    res[i] = b
                else:
                    res[i] = a + matchLen(S, a, r+1)
                    l = i
                    r = i + res[i] - 1
            else:
                res[i] = matchLen(S, 0, i)
                if res[i] > 0:
                    l = i
                    r = i + res[i] - 1
        return res

def badChar(S):
    # Returns array indexed by the position of character in English alphabet.
    if len(S) == 0:
        return [[] for a in range(26)]
    else:
        res = [[-1] for a in range(26)]
        al = [-1 for a in range(26)]
        for i, c in enumerate(S):
            al[charIndex(c)] = i
            for j, a in enumerate(al):
                res[j].append(a)
        return res

def goodSuffix(S):
    # Returns array for good suffix
    res = [-1 for c in S]
    N = preprocess(S[::-1]) # S[::-1] reverses S
    N.reverse()
    for j in range(0, len(S)-1):
        i = len(S) - N[j]
        if i != len(S):
            res[i] = j
    return res

def fullShift(S):
    # Returns array of special case of the good suffix rule
    res = [0 for c in S]
    Z = preprocess(S)
    l = 0
    for i, x in enumerate(reversed(Z)):
        l = max(x, l) if x == i+1 else l
        res[-i-1] = l
    return res

def stringSearch(sub, S):
    # Finds sub string in S string using Boyer-Moore pattern matching.
    if len(sub) == 0 or len(S) == 0 or len(S) < len(sub):
        return []
    else:
        res = []
        # Preprocessing
        arrR = badChar(sub)
        arrL = goodSuffix(sub)
        arrF = fullShift(sub)
        subLen = len(sub) - 1
        prevSubLen = -1
        while subLen < len(S):
            i = len(sub) - 1
            subLen_c = subLen
            while i >= 0 and subLen_c > prevSubLen and sub[i] == S[subLen_c]:
                i -= 1
                subLen_c -= 1
            if i == -1 or subLen_c == prevSubLen:
                res.append(subLen - len(sub) + 1)
                subLen += len(sub)-arrF[1] if len(sub) > 1 else 1
            else:
                charShift = i - arrR[charIndex(S[subLen_c])][i]
                if i+1 == len(sub):
                    suffixShift = 1
                elif arrL[i+1] == -1:
                    suffixShift = len(sub) - arrF[i+1]
                else:
                    suffixShift = len(sub) - arrL[i+1]
                shift = max(charShift, suffixShift)
                prevSubLen = subLen if shift >= i+1 else prevSubLen
                subLen += shift
        return res
