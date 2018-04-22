def charIndex(ch):
    return ord(ch.lower()) - 97 # start from 'a'

def matchLen(S, i, j):
    # counts elements of the match of the substrings of S beginning at i and j.
    if i == j:
        return len(S) - i
    else:
        match_count = 0
        while i < len(S) and j < len(S) and S[i] == S[j]:
            match_count += 1
            i += 1
            j += 1
        return match_count

def preprocess(S):
    # Returns res, the Fundamental Preprocessing of S.
    if len(S) == 0: # Base 0 : Handles case of empty string
        return []
    elif len(S) == 1: # Base 1 : Handles case of single-character string
        return [1]
    else: # recursive: more than one character
        res = [0 for x in S]
        res[0] = len(S)
        res[1] = matchLen(S, 0, 1)
        for i in range(2, 1+res[1]): # Optimization from exercise 1-5
            res[i] = res[1]-i+1
        # Defines lower and upper limits of res-box
        l = 0
        r = 0
        for i in range(2 + res[1], len(S)):
            if i <= r: # i falls within existing res-box
                b = res[i - l]
                a = r - i + 1
                if b < a: # b ends within existing res-box
                    res[i] = b
                else: # b ends at or after the end of the res-box, we need to do an explicit match to the right of the res-box
                    res[i] = a + matchLen(S, a, r+1)
                    l = i
                    r = i+res[i]-1
            else: # i does not reside within existing res-box
                res[i] = matchLen(S, 0, i)
                if res[i] > 0:
                    l = i
                    r = i + res[i] - 1
        return res

def badChar(S):
    # Generates res for S, which is an array indexed by the position of some character c in the
    # English alphabet. At that index in res is an array of length |S|+1, specifying for each
    # index i in S (plus the index after S) the next location of character c encountered when
    # traversing S from right to left starting at i. This is used for a constant-time lookup
    # for the bad character rule in the Boyer-Moore string search algorithm, although it has
    # a much larger size than non-constant-time solutions.
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
    # Generates res for S, an array used in the implementation of the strong good suffix rule.
    # L[i] = k, the largest position in S such that S[i:] (the suffix of S starting at i) matches
    # a suffix of S[:k] (a substring in S ending at k). Used in Boyer-Moore, L gives an amount to
    # shift P relative to T such that no instances of P in T are skipped and a suffix of P[:L[i]]
    # matches the substring of T matched by a suffix of P in the previous match attempt.
    # Specifically, if the mismatch took place at position i-1 in P, the shift magnitude is given
    # by the equation len(P) - L[i]. In the case that L[i] = -1, the full shift table is used.
    # Since only proper suffixes matter, L[0] = -1.
    res = [-1 for c in S]
    N = preprocess(S[::-1]) # S[::-1] reverses S
    N.reverse()
    for j in range(0, len(S)-1):
        i = len(S) - N[j]
        if i != len(S):
            res[i] = j
    return res

def fullShift(S):
    # Generates res for S, an array used in a special case of the good suffix rule in the Boyer-Moore
    # string search algorithm. F[i] is the length of the longest suffix of S[i:] that is also a
    # prefix of S. In the cases it is used, the shift magnitude of the pattern P relative to the
    # text T is len(P) - F[i] for a mismatch occurring at i-1.
    res = [0 for c in S]
    Z = preprocess(S)
    l = 0
    for i, x in enumerate(reversed(Z)):
        l = max(x, l) if x == i+1 else l
        res[-i-1] = l
    return res

def stringSearch(sub, S):
    # Implementation of the Boyer-Moore string search algorithm. This finds all occurrences of sub
    # in S, and incorporates numerous ways of pre-processing the pattern to determine the optimal
    # amount to shift the string and skip comparisons.
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
