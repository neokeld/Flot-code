
import math as mth
import MSTKruskal as K
import numpy as np

def calculDisEuclidienne(path):
	
	f = open(path,"r")
	nodes=[]
	X=[]
	Y=[]
	for line in f:
		words=line.split()
		nodes.append(int(words[0]))
		X.append(int(words[1]))
		Y.append(int(words[2]))
	
	n=len(nodes)
	M=n*[0]
	for i in range(n):
		M[i] = n*[0]
	for i in range(n):
		for j in range(n):
			M[i][j]=mth.sqrt((X[i]-X[j])**2+(Y[i]-Y[j])**2)
	return np.array(M)
	
F=K.MinimumSpanningTree(calculDisEuclidienne("./dev/data/n10-1"))
print(F)
print(K.convertToAdjacent(F))
