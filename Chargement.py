
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

	
def getLevels(L):
	n=len(L)
	processedNodes=[]
	lev=[]
	lev.append([0])
	processedNodes.append(0)
	i=0
	j=0
	while j!=n-1:
		lev.append([])
		for v in lev[i]:
			for e in L[v]:
				if e not in processedNodes:
					lev[i+1].append(e)
					processedNodes.append(e)
			j+=1
		i+=1
	return lev

def frec(v,L,k,adL,Lev,i,Processed):
	if len(L)==k:
		return L
	else:
		for e in adL[v]:
			if e in Lev[i-1]:
				L.append(e);
				if len(L)!=k:
					Processed.append(e)
				frec(e,L,k,adL,Lev,i-1,Processed)
	

def getCycles(Lev,adL,k):
	cycles=[]
	Processed=[]
	nbLevs=len(Lev)
	for i in range(nbLevs-1,0,-1):
		if k==i:
			Processed=[]
		for e in Lev[i]:
			if e not in Processed:
				T=[];
				T.append(e)
				frec(e,T,k,adL,Lev,i,Processed)
				cycles.append(T)
	
	stop=False
	twoCycles=[]
	while not stop:
		n=len(cycles)
		if len(cycles[n-1])==2:
			twoCycles.append(cycles[n-1])
			cycles.pop(n-1)
		else:
			stop=True
	
	n=len(twoCycles)
	if n==0:
		return cycles
	else:
		if n==1:
			twoCycles[0].append(adL[twoCycles[0][0]][0])
		else:
			twoCycles[0].append(twoCycles[1][0])
			for i in range(len(twoCycles)-1):
				twoCycles[i+1].append(twoCycles[i][0])
		for E in twoCycles:
			cycles.append(E)
		return cycles


M=EuclideanDistMatrix("./dev/data/n40-2")
print(M)
F=K.MinimumSpanningTree(M)
print(F)
adL=K.convertToAdjacentN(F)
print(adL)
Lev=getLevels(adL)
print(Lev)
# T=[]
# T.append(6)
# print(frec(6,T,3,Z,L,5))
# print(T)
print(getCycles(Lev,adL,3))

