"""MinimumSpanningTree.py

Kruskal's algorithm for minimum spanning trees. D. Eppstein, April 2006.
"""

from UnionFind import UnionFind
import numpy as np

def MinimumSpanningTree(G):
	"""
	Return the minimum spanning tree of an undirected graph G.
	G should be represented in such a way that G[u][v] gives the
	length of edge u,v, and G[u][v] should always equal G[v][u].
	The tree is returned as a list of edges.
	"""
    
    # Kruskal's algorithm: sort edges by weight, and add them one at a time.
    # We use Kruskal's algorithm, first because it is very simple to
    # implement once UnionFind exists, and second, because the only slow
    # part (the sort) is sped up by being built in to Python.

	subtrees = UnionFind()
	(n,m)=G.shape
	tree = []
	edges = [(G[u][v],u,v) for u in np.arange(n) for v in np.arange(m)]
	edges.sort()
	for W,u,v in edges:
		if subtrees[u] != subtrees[v]:
			tree.append((u,v))
		subtrees.union(u,v)
	return tree  


G=np.array([[0,1,2,5],[1,0,2,3],[2,2,0,1],[5,3,1,0]])
print(MinimumSpanningTree(G))