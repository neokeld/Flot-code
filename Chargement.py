
import math as mth
import MSTKruskal as K
import numpy as np

def EuclideanDistMatrix(path):
	#fonction qui charge un fichier de test et renvoie la matrice de couts 
	#cout = distance euclidienne
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
	#retourne une liste de liste de noeud classe par niveaux
	#par defaut le niveau 0 contient uniquement le noeud 0 (la racine)
	n=len(L)
	processedNodes=[]
	lev=[]
	lev.append([0])
	processedNodes.append(0)
	i=0
	while len(processedNodes)<n:
		lev.append([])
		for v in lev[i]:
			for e in L[v]:
				if e not in processedNodes:
					lev[i+1].append(e)
					processedNodes.append(e)
		i+=1
	return lev

def depthSearch(v,L,k,adL,Lev,i,nodesInCycle):
	#fait un parcours en profondeur de longueur k a partir du noeud v
	if len(L)==k:
		return L
	else:
		for e in adL[v]:
			if e in Lev[i-1]:
				L.append(e);
				if len(L)!=k:
					nodesInCycle.append(e)
				depthSearch(e,L,k,adL,Lev,i-1,nodesInCycle)
	

	
	
def getCycles(Lev,adL,k):
	#recherches de cycles de longeur k en remontant des feuilles de l'arbre
	cycles=[]
	nodesInCycle=[]
	nbLevs=len(Lev)
	for i in range(nbLevs-1,0,-1):
		for e in Lev[i]:
			if e not in nodesInCycle:
				T=[];
				T.append(e)
				depthSearch(e,T,k,adL,Lev,i,nodesInCycle)
				cycles.append(T)
	
	#Traitement des restes de longueur 2 au cas ou il y'en a
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
			if adL[twoCycles[0][0]][0]==twoCycles[0][1]:
				twoCycles[0].append(adL[twoCycles[0][0]][1])
			else:
				twoCycles[0].append(adL[twoCycles[0][0]][0])
		else:
			twoCycles[0].append(twoCycles[1][0])
			for i in range(len(twoCycles)-1):
				twoCycles[i+1].append(twoCycles[i][0])
		for E in twoCycles:
			cycles.append(E)
		return cycles

if __name__ == '__main__':

    M=EuclideanDistMatrix("./dev/data/n10-5")
    print(M)
    F=K.MinimumSpanningTree(M)
    print(F)
    adL=K.convertToAdjacentN(F)
    print(adL)
    Lev=getLevels(adL)
    print(Lev)
    print(getCycles(Lev,adL,3))

