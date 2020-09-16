# Returns list difference. Keeps correct order of elements (unlike when using set difference)
def listDiff(lisA, lisB):
    return [i for i in lisA + lisB if i not in lisA or i not in lisB]