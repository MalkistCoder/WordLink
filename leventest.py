def levenDist(string1: str, string2: str) -> int:
    len1 = len(string1)
    len2 = len(string2)
    
    if len2 == 0:
        return len1
    elif len1 == 0:
        return len2
    elif string1[0] == string2[0]:
        return levenDist(stringTail(string1), stringTail(string2))
    else:
        dist_tail1_2 = levenDist(stringTail(string1), string2)
        dist_1_tail2 = levenDist(string1, stringTail(string2))
        dist_tail1_tail2 = levenDist(stringTail(string1), stringTail(string2))
        
        return 1 + min(dist_tail1_2, dist_1_tail2, dist_tail1_tail2)
        
def stringTail(string: str) -> str:
    return string[1:]
