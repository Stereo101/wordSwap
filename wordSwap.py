import sys
from heapq import *

INFINITY = 99999999

class wordNode:
	def __lt__(self,other):
		return self.dist < other.dist
	def __init__(self,word):
		self.word = word
		self.adj = []
		self.dist = INFINITY
		self.prev = 0

	def addEdge(self,wordNodePointer):
		if(wordNodePointer not in self.adj):
			self.adj.append(wordNodePointer)
			return True
		return False

	def hasEdge(self,word):
		for e in self.adj:
			if(e.word == word): return True
		return False

def dijkstra(wordA,wordB,wordDict):
	nodeHold = 0
	start = wordDict[wordA]
	goal = wordDict[wordB]
	unvisited = []
	heapify(unvisited)
	start.dist = 0
	for n in wordDict.values():
		heappush(unvisited,n)

	
	while len(unvisited)!=0:
		u = heappop(unvisited)
		if(u.dist == INFINITY):
			return False
		print(u.word,u.dist)
		for edge in u.adj:
			alt = u.dist + 1
			if alt < edge.dist:
				edge.dist = alt
				edge.prev = u
		heapify(unvisited)

		if goal not in unvisited:
			return True

def buildWordGraphDict(dictFile,wordLength):
	wordDict = {}
	for w in open(dictFile,"r").read().splitlines():
		if(len(w) == wordLength):
			wordDict[w] = wordNode(w)
			for i in range(len(w)):
				for letter in range(0,26):
					whold = w[0:i] + chr(letter+97) + w[i+1:wordLength]
					if(whold in wordDict and not wordDict[w].hasEdge(whold) and whold != w):
						wordDict[w].addEdge(wordDict[whold])
						wordDict[whold].addEdge(wordDict[w])
	return wordDict


if(len(sys.argv) < 3):
	print("Enter 2 words as command line args")
	sys.exit()

if(len(sys.argv[1]) != len(sys.argv[2])):
	print("Words are a differnt length, not possible")
	sys.exit()

wordLength = len(sys.argv[1])

wordDict = buildWordGraphDict("wordlist",wordLength)
wordCount = len(wordDict)
if(sys.argv[1] not in wordDict):
	print(sys.argv[1],"is not in this dictionary")
	sys.exit()
if(sys.argv[2] not in wordDict):
	print(sys.argv[2],"is not in this dictionary")
	sys.exit()

print(wordCount,"words of length",wordLength,"were loaded.")
dijkstra(sys.argv[1],sys.argv[2],wordDict)

if(wordDict[sys.argv[2]].dist == INFINITY):
	print("No possible path")
else:
	print("The distance between",sys.argv[1],"and",sys.argv[2],"is",wordDict[sys.argv[2]].dist)
	path = []
	cur = wordDict[sys.argv[2]]
	while(cur != wordDict[sys.argv[1]]):
		path.insert(0,cur.word)
		cur=cur.prev
	print(sys.argv[1])
	for w in path:
		print(w)
