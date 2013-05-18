
import math as mth
import MSTKruskal as K
import numpy as np

def EuclideanDistMatrix(path):
	
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
	M=[n*[0] for i in range(n)]

	for i in range(n):
		for j in range(n):
			M[i][j]=np.round(mth.sqrt((X[i]-X[j])**2+(Y[i]-Y[j])**2),2)
	return np.array(M)
	
M=EuclideanDistMatrix("./dev/data/n10-1")
print(M)
F=K.MinimumSpanningTree(M)
print(F)
print(K.convertToAdjacent(F,M))
