import sys
from heapq import *

##I am aware this isn't true
##It just needs to be bigger than the dictionary is in size
INFINITY = 99999999

class wordNode:
	def __init__(self,word):
		self.word = word
		self.adj = []

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
	frontier = []
	heappush(frontier,wordDict[wordA])
	visited = {}
	prev = {}
	dist = {}
	dist[wordA] = 0	
	prev[wordA] = wordDict[wordA]
	goal = wordDict[wordB]
	while len(frontier)!=0:
		u = heappop(frontier)
		visited[u] = True
		for edge in u.adj:
			if edge.word not in dist:
				dist[edge.word] = INFINITY
			alt = dist[u.word] + 1
			if alt < dist[edge.word]:
				dist[edge.word] = alt
				prev[edge.word] = u
			if(edge not in visited and edge not in frontier):
				heappush(frontier,edge)
		if wordB in prev:
			result = []
			u = goal
			while u.word != wordA:
				result.insert(0,u.word)
				u = prev[u.word]
			return  result
	return False

def buildWordGraphDict(dictFile,wordLength):
	wordDict = {}
	edgeDict = {}
	for w in open(dictFile,"r").read().splitlines():
		if(len(w) == wordLength):
			wordDict[w] = wordNode(w)
			for i in range(len(w)):
				whold = w[0:i] + '*' + w[i+1:wordLength]
				if(whold not in edgeDict):
					edgeDict[whold] = [w]
				else:
					for e in edgeDict[whold]:
						wordDict[w].addEdge(wordDict[e])
						wordDict[e].addEdge(wordDict[w])
					edgeDict[whold].append(w)
	del edgeDict
	return wordDict

if __name__ == "__main__":
	if(len(sys.argv) < 3):
		print("Enter 2 words of equal size as command line args")
		sys.exit()

	if(len(sys.argv[1]) != len(sys.argv[2])):
		print("Words are a differnt length, not possible")
		sys.exit()

	wordLength = len(sys.argv[1])

	wordDict = buildWordGraphDict("wordlist",wordLength)
	if(sys.argv[1] not in wordDict):
		print(sys.argv[1],"is not in this dictionary")
		sys.exit()
	if(sys.argv[2] not in wordDict):
		print(sys.argv[2],"is not in this dictionary")
		sys.exit()

	print("%d words of length %d were loaded" % (len(wordDict),wordLength))
	result = dijkstra(sys.argv[1],sys.argv[2],wordDict)

	if(type(result) is not type([])):
		print("No possible path")
	else:
		print("The distance between %s and %s is %d" % (sys.argv[1],sys.argv[2],len(result)))
		for w in result:
			print(w)
