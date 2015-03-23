import random

class node():
    def __init__(self, n):
        self.id = n
        self.parents = []
        self.children = []
        self.allParents = []
        self.allChildren = []
    def addChild(self, child):
        self.children.append(child.id)
    def addParent(self, parent):
        self.parents.append(parent.id)

def addEdge(parent, child):
    parent.addChild(child)
    child.addParent(parent)

def getChildren(node, graph):
    if node.allChildren != []:
        return node.allChildren
    else:
        res = set()
        for childID in node.children:
            res.add(childID)
            res |= getChildren(graph[childID], graph)
    return res

def getParents(node, graph):
    if node.allParents != []:
        return node.allParents
    else:
        res = set()
        for parentID in node.parents:
            res.add(parentID)
            res |= getParents(graph[parentID], graph)
    return res

def genGraph(n, p):
    graph = []
    for i in range(n):
        graph.append(node(i))
    for i in range(n):
        for j in range((i + 1), n):
            if (random.random() < p):
                addEdge(graph[i], graph[j])
    for i in range(n):
        graph[i].allParents = getParents(graph[i], graph)
        graph[i].allChildren = getChildren(graph[i], graph)
    return(graph)

def findCausal(graph):
    res = set()
    for node in graph:
        res |= set([(node.id, x) for x in getChildren(node, graph)])
    return res

def findCor(graph):
    res = set()
    for node in graph:
        children = getChildren(node, graph)
        res |= set([(node.id, x) for x in children])
        pairs = [(x, y) for x in children for y in children if x < y]
        res |= set(pairs)
    return res

def experiment(n, p):
    g = genGraph(n, p)
    return (float(len(findCausal(g))) / float(len(findCor(g))))

for i in range(500, 550):
    lst = [experiment(i, .01) for x in range(20)]
    print (float(sum(lst))/float(len(lst)))
