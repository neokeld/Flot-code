#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import numpy as np

class Edge:
    def __init__(self, n1, n2, w):
	self.node1 = n1
	self.node2 = n2
	self.weight = n3

# Stocke un graphe sous forme d'une matrice d'adjacence
# et réalise un certain nombre d'opérations dessus
class Graph:
    def __init__(self):
	self.matrix = np.array([[0,146,188],
				[1,82,46],
				[2,37,14],
				[3,100,13],
				[4,158,157]) # Création de la matrice
	# Construire les edges	
    def kruskal(self):
	self.matrix.sort(axis=0, kind='mergesort')  # Tri, les algorithmes disponibles sont 'quicksort', 'mergesort' et 'heapsort'
    def show(self):
	print self.matrix

if __name__ == '__main__':
    g = Graph()
    g.show()
    g.kruskal()
    g.show()

