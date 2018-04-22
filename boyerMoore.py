def alphabetIndex(ch):
    # Returns the index of the given character in the English alphabet, counting from 0.
    return ord(ch.lower()) - 97 # 'a' is ASCII character 97

def matchLength(S, i, j):
    # Returns the length of the match of the substrings of S beginning at i and j.
    if i == j:
        return len(S) - i
    else:
        match_count = 0
        while i < len(S) and j < len(S) and S[i] == S[j]:
            match_count += 1
            i += 1
            j += 1
        return match_count

def fundamentalPreprocess(S):
    # Returns res, the Fundamental Preprocessing of S. res[i] is the length of the substring
    # beginning at i which is also a prefix of S. This pre-processing is done in O(n) time,
    # where n is the length of S.
    if len(S) == 0: # Base 0 : Handles case of empty string
        return []
    if len(S) == 1: # Base 1 : Handles case of single-character string
        return [1]
    else:
        res = [0 for x in S]
        res[0] = len(S)
        res[1] = matchLength(S, 0, 1)
        for i in range(2, 1+res[1]): # Optimization from exercise 1-5
            res[i] = res[1]-i+1
        # Defines lower and upper limits of res-box
        l = 0
        r = 0
        for i in range(2+res[1], len(S)):
            if i <= r: # i falls within existing res-box
                k = i-l
                b = res[k]
                a = r-i+1
                if b < a: # b ends within existing res-box
                    res[i] = b
                else: # b ends at or after the end of the res-box, we need to do an explicit match to the right of the res-box
                    res[i] = a+matchLength(S, a, r+1)
                    l = i
                    r = i+res[i]-1
            else: # i does not reside within existing res-box
                res[i] = matchLength(S, 0, i)
                if res[i] > 0:
                    l = i
                    r = i+res[i]-1
        return res

def badCharacterTable(S):
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
        alpha = [-1 for a in range(26)]
        for i, c in enumerate(S):
            alpha[alphabetIndex(c)] = i
            for j, a in enumerate(alpha):
                res[j].append(a)
        return res

def goodSuffixTable(S):

    # Generates res for S, an array used in the implementation of the strong good suffix rule.
    # L[i] = k, the largest position in S such that S[i:] (the suffix of S starting at i) matches
    # a suffix of S[:k] (a substring in S ending at k). Used in Boyer-Moore, L gives an amount to
    # shift P relative to T such that no instances of P in T are skipped and a suffix of P[:L[i]]
    # matches the substring of T matched by a suffix of P in the previous match attempt.
    # Specifically, if the mismatch took place at position i-1 in P, the shift magnitude is given
    # by the equation len(P) - L[i]. In the case that L[i] = -1, the full shift table is used.
    # Since only proper suffixes matter, L[0] = -1.

    res = [-1 for c in S]
    N = fundamentalPreprocess(S[::-1]) # S[::-1] reverses S
    N.reverse()
    for j in range(0, len(S)-1):
        i = len(S) - N[j]
        if i != len(S):
            res[i] = j
    return res

def fullShiftTable(S):

    # Generates res for S, an array used in a special case of the good suffix rule in the Boyer-Moore
    # string search algorithm. F[i] is the length of the longest suffix of S[i:] that is also a
    # prefix of S. In the cases it is used, the shift magnitude of the pattern P relative to the
    # text T is len(P) - F[i] for a mismatch occurring at i-1.

    res = [0 for c in S]
    Z = fundamentalPreprocess(S)
    longest = 0
    for i, zv in enumerate(reversed(Z)):
        longest = max(zv, longest) if zv == i+1 else longest
        res[-i-1] = longest
    return res

def stringSearch(sub, S):

    # Implementation of the Boyer-Moore string search algorithm. This finds all occurrences of sub
    # in S, and incorporates numerous ways of pre-processing the pattern to determine the optimal
    # amount to shift the string and skip comparisons.

    if len(sub) == 0 or len(S) == 0 or len(S) < len(sub):
        return []
    else:
        matches = []
        # Preprocessing
        arr_R = badCharacterTable(sub)
        arr_L = goodSuffixTable(sub)
        arr_F = fullShiftTable(sub)

        k = len(sub) - 1
        previous_k = -1
        while k < len(S):
            i = len(sub) - 1
            h = k
            while i >= 0 and h > previous_k and sub[i] == S[h]:
                i -= 1
                h -= 1
            if i == -1 or h == previous_k:
                res.append(k - len(sub) + 1)
                k += len(sub)-arr_F[1] if len(sub) > 1 else 1
            else:
                char_shift = i - arr_R[alphabetIndex(S[h])][i]
                if i+1 == len(sub):
                    suffix_shift = 1
                elif arr_L[i+1] == -1:
                    suffix_shift = len(sub) - arr_F[i+1]
                else:
                    suffix_shift = len(sub) - arr_L[i+1]
                shift = max(char_shift, suffix_shift)
                previous_k = k if shift >= i+1 else previous_k
                k += shift
        return res
