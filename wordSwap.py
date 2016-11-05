import sys
from collections import OrderedDict

##I am aware this isn't true
##It just needs to be bigger than the dictionary is in size
INFINITY = 99999999

class wordNode:
	def __init__(self,word):
		self.word = word
		self.adj = {}
	
	def __lt__(self,other):
		return False
	
	def addEdge(self,wordNodePointer):
		if(wordNodePointer.word not in self.adj):
			self.adj[wordNodePointer.word] = wordNodePointer
			return True
		return False

	def hasEdge(self,word):
		return word in self.adj

def dijkstra(wordA,wordB,wordDict):
	frontier = OrderedDict()
	frontier[wordA] = True
	visited = {}
	prev = {}
	dist = {}
	dist[wordA] = 0	
	prev[wordA] = wordDict[wordA]
	goal = wordDict[wordB]
	while frontier:
		u = wordDict[frontier.popitem(last=False)[0]]
		visited[u.word] = True
		for edge in u.adj:
			edgeP = wordDict[edge]
			if edge not in dist:
				dist[edge] = INFINITY
			alt = dist[u.word] + 1
			if alt < dist[edge]:
				dist[edge] = alt
				prev[edge] = u
			if(edge not in visited and edge not in frontier):
				frontier[edge] = True
		if wordB in prev:
			result = []
			u = goal
			while u.word != wordA:
				result.insert(0,u.word)
				u = prev[u.word]
			result.insert(0,wordA)
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
		print("Words are a different length, not possible")
		sys.exit()

	wordLength = len(sys.argv[1])

	wordDict = buildWordGraphDict("wordlist",wordLength)
	for arg in sys.argv[1:]:
		if(arg not in wordDict):
			print("%s is not in this dictionary" % arg)
			sys.exit()

	print("%d words of length %d were loaded" % (len(wordDict),wordLength))
	result = dijkstra(sys.argv[1],sys.argv[2],wordDict)

	if(type(result) is not type([])):
		print("No possible path")
	else:
		print("The distance between %s and %s is %d" % (sys.argv[1],sys.argv[2],len(result)-1))
		for w in result:
			print(w)
