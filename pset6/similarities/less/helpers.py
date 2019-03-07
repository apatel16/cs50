from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    matches = []

    file1 = a.split("\n")
    file2 = b.split("\n")

    for line in file1:
        if line in file2:
            matches.append(line)

    return set(matches)


def sentences(a, b):
    """Return sentences in both a and b"""
    matches = []

    file1 = sent_tokenize(a)
    file2 = sent_tokenize(b)

    for sent in file1:
        if sent in file2:
            matches.append(sent)

    return set(matches)


def get_subs(a, n):
    subs = []
    _string = a.replace(" ", "")

    for i in range(len(a)-n+1):
        subs.append(a[i:i+n])

    return subs


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    matches = []

    file1 = get_subs(a, n)
    file2 = get_subs(b, n)

    for sub in file1:
        if sub in file2:
            matches.append(sub)

    return set(matches)
