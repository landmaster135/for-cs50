from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    # TODO

    # inp1 = a # File1's name
    # inp2 = b # File2's name

    # inp1_file = open(inp1, mode='r', encoding='utf-8') # open Flie1
    # inp2_file = open(inp2, mode='r', encoding='utf-8') # open File2
    # inp1_content = inp1_file.read() # read File1
    # inp2_content = inp2_file.read() # read File2

    # inp1_list = inp1_content.split('\n') # File1's content to list
    # inp2_list = inp2_content.split('\n') # File2's content to list

    inp1_list = a.split('\n') # File1's content to list
    inp2_list = b.split('\n') # File2's content to list

    same_list = []
    for i in inp1_list:
        if i == inp2_list[inp1_list.index(i)]:
            same_list.append(i) # append same line.
        else:
            same_list.append('') # append void.

    same_set = set(same_list)
    return same_set


def sentences(a, b):
    """Return sentences in both a and b"""

    # TODO
    # inp1 = a # File1's name
    # inp2 = b # File2's name

    # inp1_file = open(inp1, mode='r', encoding='utf-8') # open Flie1
    # inp2_file = open(inp2, mode='r', encoding='utf-8') # open File2
    # inp1_content = inp1_file.read() # read File1
    # inp2_content = inp2_file.read() # read File2

    # inp1_list = [] # to own File1's content
    # inp2_list = [] # to own File2's content

    # inp1_list = sent_tokenize(inp1_content) # File1's content to list
    # inp2_list = sent_tokenize(inp2_content) # File2's content to list

    inp1_list = sent_tokenize(a) # File1's content to list
    inp2_list = sent_tokenize(b) # File2's content to list

    same_list = []
    for i in inp1_list:
        if i == inp2_list[inp1_list.index(i)]:
            same_list.append(i) # append same line.
        else:
            same_list.append('') # append void.

    same_set = set(same_list)
    return same_list


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # TODO
    # inp1 = a # File1's name
    # inp2 = b # File2's name

    # inp1_file = open(inp1, mode='r', encoding='utf-8') # open Flie1
    # inp2_file = open(inp2, mode='r', encoding='utf-8') # open File2
    # inp1_content = inp1_file.read() # read File1
    # inp2_content = inp2_file.read() # read File2

    inp1_list = [] # to own File1's content
    inp2_list = [] # to own File2's content

    # for i in inp1_content:
    #     x = inp1_content.index(i)
    #     inp1_list.append(inp1_content[x:x+n]) # File1's content to list

    # for i in inp2_content:
    #     x = inp2_content.index(i)
    #     inp2_list.append(inp2_content[x:x+n]) # File2's content to list

    for i in a:
        x = a.index(i)
        inp1_list.append(a[x:x+n]) # File1's content to list

    for i in b:
        x = b.index(i)
        inp2_list.append(b[x:x+n]) # File2's content to list

    same_list = []
    for i in inp1_list:
        if i == inp2_list[inp1_list.index(i)]:
            same_list.append(i) # append same line.
        else:
            same_list.append('') # append void.

    same_set = set(same_list)
    return same_list


# lines('inputs/compare-1.c', 'inputs/compare-2.c')
# sentences('inputs/Genesis-ESV.txt', 'inputs/Genesis-KJV.txt')
# substrings('inputs/LesMis1.txt', 'inputs/LesMis2.txt', 3)