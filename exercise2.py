'''
Lexicographical order is often known as alphabetical order when dealing with strings. A string is greater than another string if it comes later in a lexicographically sorted list.
Given a word, create a new word by swapping some or all of its characters. This new word must meet two criteria:
●       It must be greater than the original word
●       It must be the smallest word that meets the first condition
'''

for _ in range(int(input())):
    w = input().strip()
    n = len(w)+1
    for k in range(-2,-n,-1):# read the word w from right to left,
        if w[k]<w[k+1]:# Searching for the first letter w[k] smaller than the previous (from right).
            print(w[:k],end='')# Leave the left part of the word unchanged, and print it.
            v = w[:k:-1]# The right part is to be rearranged - inversed first of all - to give the smallest possible.
            for j in range(-k-1):# Look for the right place there to insert w[k] which has been found earlier.
                if w[k]<v[j]:# Right place means the leftmost letter v[j] of the inversed right part v, which is greater than w[k].
                    print(v[j]+v[:j]+w[k]+v[j+1:])# Inversion of w[k] and v[j] completes the rearrangement of the right part,
                    break# so I print it and leave.
            else:# If only one (the rightmost) letter of the inversed right part v is greater than w[k], its inversion with w[k]
                print(v+w[k])# means just placing w[k] after the v.
            break
    else:# If no letter of the initial word w is smaller than the previous from right, i.e. the letters are decreasing in the word, 
        print('no answer')# than no rearrangement gives a lexicographically greater.
