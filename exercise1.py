'''
You are given  words. Some words may repeat. For each word, output its number of occurrences. The output order should correspond with the input order of appearance of the word. See the sample input/output for clarification.
Note: Each input line ends with a "\n" character.
Constraints:
1 ≤ n ≤ 105
The sum of the lengths of all the words do not exceed 106 All the words are composed of lowercase English letters only.
'''

from collections import OrderedDict
#define empty ordered dictionary, which counts occurences
dict = OrderedDict()

for _ in range(int(input())):
    #If input is not presented in the dictionary, then add it
    #else increment the counter
    key = input()
    if key not in dict.keys():
        dict.update({key : 1})
        continue
    dict[key] += 1

print(len(dict.keys()))
print(*dict.values())