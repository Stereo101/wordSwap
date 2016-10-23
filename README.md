Google said I should be able to do this or something.

Breakdown:

get 2 words as input

hash dictionary of all words of length == input from dictionary

while hashing the dictionary, create a graph where each word connects to other words that differ by 1 letter

do dijkstra shortest path algo on the graph

print the result
