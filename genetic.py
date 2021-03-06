#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# genetic.py - A utility class to facilitate experimentation
# with genetic algorithm concepts.
#
# Version 1.0
# Project page: http://hobbiton.thisside.net/genetic/
# This software is provided under the BSD license:

import sys, os, math, random, bisect, MSTKruskal, UnionFind, Chargement

class Genetic:

	# Initialise tous les paramètres nécessaires pour l'algorithmique génétique
	# Param : max_nb_gen : nombre maximum de generation
	def __init__(self, max_nb_gen, crossover_rate, mutation_rate, K):	
	
		print "init"
		# Topologie des noeud
		self.graph = None
		print "Graphe :"
		print self.graph
		# Liste de liste d'arêtes (constitue un chromosome)
		self.list_edge = [[0,0]]*7
		print "Arêtes :"
		print self.list_edge
		# Numéro de génération en cours
		self.nb_gen = 0
		# Max nb de générations
		self.max_nb_gen = max_nb_gen
		# Taux de croisement (%)
		self.crossover_rate = crossover_rate
		# Taux de mutation (%)
		self.mutation_rate = mutation_rate
		# Longueur de cycle Max :
		self.K = K
		# nombre de noeud
		self.nb_nodes = 0
		# liste des chromosomes, c'est notre population
		self.pop = []
		# Profondeur de parcours max
		self.profondeur = 4
		# matrice de cout WALA
		self.M = None
		# initialiser le moteur d'aléatoire
		random.seed()


	# Générer une population de départ
	def create_first_population(self):
		print "create first population"
		# création du graphe
		self.M=Chargement.EuclideanDistMatrix("./dev/data/n10-2")
		self.nb_nodes = len(self.M)
		F=MSTKruskal.MinimumSpanningTree(self.M)	
		self.graph = MSTKruskal.convertToAdjacent(F, self.M)
		# création de la première population
		adLN = MSTKruskal.convertToAdjacentN(F)
		Lev = Chargement.getLevels(adLN)
		#for cycle in Chargement.getCycles(Lev, adLN, 3):
		#    self.pop.append([int(i) for i in cycle])
		self.pop = [Chargement.getCycles(Lev, adLN, 3)]
		print self.pop
		print type(self.pop), type(self.pop[0][0])

		
	# Do probablistic crossover operation.
	def crossover_old(self, i, j):
		print "crossover"
		chrom1 = self.pop[i]
		chrom2 = self.pop[j]
		new_chrom = [[0,0]*self.K]
		# pour chaque noeud
		for k in range(nb_node):
		    # il faut choisir un cycle parmi les deux chromosomes 
		    r = random.randint(0,1)
		    if r == 0 :
			# on prend un bout de gene, ie on prend un cycle parmi tous les cycles du noeud k pour le chrom1
			new_chrom[k] = chrom1[k][random.randint(0,len(chrom1[k]))]
		    else :
			print "chrom2 : ", chrom2[k]
			new_chrom[k] = chrom2[k][random.randint(0,len(chrom2[k]))]

		print new_chrom
		self.pop.append(new_chrom)

		# maintenant on a pour chaque noeud un cycle
	
	def crossover(self, i, j):
		bebe = self.pop[i] + self.pop[j]
		#print "Oh le beau bébé ! Bienvenue à ", bebe, " fils de ", self.pop[i], " et ", self.pop[j]
		utile = [1] * len (bebe) #0 = non, 1 = peut-etre, 2 = necessaire
		#print utile
		nb_judged = 0
		while nb_judged < len (bebe):
		    i = random.randint(0, len (bebe) -1)
		    if utile[i] != 1:
			continue
		    nodes = bebe[i]
		    j = 0
		    while nodes and j < len(bebe):
			if j == i:
			    j += 1
			    continue
			else:
			    #print "---nodes : ", nodes
			    nodes_tmp = set(nodes)
			    for n in nodes:
				if bebe[j].count(n) > 0 and utile[j] >= 1:
				    #print "nodes_tmp", nodes_tmp
				    if n in nodes_tmp :
					nodes_tmp.remove(n)
			    nodes = nodes_tmp
			    j += 1
		    if nodes:
			utile[i] = 2
		    else:
			utile[i] = 0
		    nb_judged += 1
		bebe_chromo = [bebe[gene] for gene in range(len(bebe)) if utile[gene] == 2]
		self.pop.append(bebe_chromo)
	
	# fait l'ensemble des crossovers pour une génération
	def crossover_all(self):
	    #print "debut crossover all"
	    for i in range(len(self.pop)):
		r = random.random()
		#print "r : ", r
		if r <= crossover_rate :
		    # ce chromosome va subir un crossover
		    ri = random.randint(0, len(self.pop) - 1)
		    #print "ri : ", ri, "i : ", i
		    if ri != i :
			#print "appel crossover"
			self.crossover(i,ri)
	    #print self.pop


	# Fait une mutation i(probabiliste, peut ne pas faire de mutation dans certains cas)
	def mutate_old(self, chromo, cycle):
		print "mutate"
		# on prend 1 noeud au hasard
		n1 = random.randint(0, len(cycle)-3)
		# on choisi 1 noeud à distance 2 du premier
		n2 = cycle[n1+2]
		# on supprime l'arrête suivant le n1
		nTmp = cycle.pop(n1+1)
		# si trouvé ou non
		found = False
		# noeud courant
		current_node = n1
		# chemin de n1 a n2
		# on parcours en largeurs les voisins
		# pour trouver un chemin entre les deux noeuds différent du chemin original
		found = False
		nodes_parcourues = [n1]
		f = [n1]
		while len(f) > 0 and not found:
		    current_node = f[0]
		    if current_node == n2 :
			found = True
			continue

		    f = f[1:]
		    for node, cout in self.graph[current_node] :
			if node not in nodes_parcourues :
			    nodes_parcourues.append(node)
			    f.append(node)

		if f != []:
		    f.pop(0)
		    # on ajoute le chemin f trouvé dans l'ancien cycle
		    cycle[n1+1:n1+1] = f
		# on ajoute le cycle dans le chromosome
		chromo.append(cycle)
		# trier le chromosome par premier noeud de chaque gène
		chromo.sort()

	def mutate(self, chromo):
	    #print "mutate"
	    for gene in chromo:
		n1 = random.randint(0, len(gene) -1)
		n2 = random.randint(0, len(gene) -1)
		tmp = gene[n1]
		gene[n1] = gene[n2]
		gene[n2] = tmp
	    mutingNodes = []
	    for gene in chromo:
		n1 = random.randint(0, len(gene) -1)
		mutingNodes.append((gene.pop(n1), n1))
	    random.shuffle(mutingNodes)
	    i = 0
	    for n in mutingNodes:
		chromo[i].insert(n[1], n[0])
		i += 1


	# fitness : évaluer un chromosome
	def fitness(self, chromo):
		#print "fitness"
		
		m = set()
		for gene in chromo:
		    for i in range(-1 , len(gene) - 1):
			m.add((min(gene[i], gene[i+1]), max(gene[i], gene[i+1])))
		cout = 0
		for arete in m:
		    cout += self.M[arete[0]][arete[1]]
		return  -1 * cout

	# Calculate value for the current chromosome generation.
	def calculate_generation(self):
		#print "calculate generation"
		# Result generated by the current generation of chromosome.
		self.current_result = 0
		# String generated from chromosome operators, used for evaluation.
		self.eval_string = ""
		# Last type of gene encountered in the chromosome.  Needed for type alternation.
		last_type = ""
		
		# Mutate and crossover operations on chromosome
	
		self.mutate()
	#	self.crossover()
		
		i=0
		while (i < len(self.chromosome)):
			# Step through each gene in the chromosome.
			chrom_string = ""
			current_chromosome = self.chromosome[i:i+self.bitcount+1]
			if (len(current_chromosome) < self.bitcount+1):
				if (last_type == "operator"):
					self.eval_string=self.eval_string[:-1]
				break
			x=0
			for x in range(self.bitcount+1):
				chrom_string = chrom_string + current_chromosome[x]
				
			print 'chrom_string: %s' % (chrom_string)
			try:
				chromosome_operator = self.chromosome_map[chrom_string]['op']
				chromosome_type = self.chromosome_map[chrom_string]['type']
				# Skip addition to operator string if next gene is of same type.
				if (last_type == "") or (chromosome_type != last_type):
					if (i == 0 ) or \
					(i == len(self.chromosome) - (self.bitcount+1)) or \
					(self.eval_string == "") and \
		    ulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbulbnodes(chromosome_type == "operator"):
						pass		
					else:
						self.eval_string = self.eval_string + chromosome_operator
						last_type = chromosome_type
			except KeyError:
				pass
			i = i + self.bitcount + 1
				
		# Evaluate the completed operator string.
		if (self.eval_string != ""):
			print 'eval string is: %s' % (self.eval_string)
			try:
				self.current_result = float(eval(self.eval_string))
			except ZeroDivisionError:
				self.current_result = None
		else:
			self.current_result = None
		self.generation = self.generation + 1

	def selectionNat(self, nb_surv):
		bests = []
		bestsCost = []
		ind = 0
		for ch in self.pop:
			if len(bests) == 0:
				bests.append(ch)
				bestsCost.append(self.fitness(ch))
			else:
				fit = self.fitness(ch)
				#print "fit : ", fit
				#print "bestsCost : ", bestsCost
				ind = bisect.bisect_left(bestsCost, fit)
				bests.insert(ind, ch)
				bestsCost.insert(ind, fit)
				if len(bests) > nb_surv:
					bests.pop(0)
					bestsCost.pop(0)
		self.pop = bests
		print "Da best IZ :", self.fitness(bests[0])
		print bests[0]

if __name__ == '__main__':
    max_nb_gen = 20
    crossover_rate = 0.8
    mutation_rate = 0.3
    K = 4
    nb_node = 7
    nb_mutations = 3
    nb_surv = 25
    #g = Genetic(max_nb_gen, crossover_rate, mutation_rate, K, nb_node )
    #g.create_first_population()
    #g.crossover_all()
    #chromo = []
    #cycle = [0, 2, 3, 6, 5, 1]
    #g.mutate(chromo, cycle)
    #print "chromo :"
    #print chromo
    g = Genetic(max_nb_gen, crossover_rate, mutation_rate, K)
    g.create_first_population()
    g.pop = g.pop * 30
    print g.graph
    print g.pop
    for i in range(20):
	for ch in g.pop:
	    for i in range(nb_mutations):
		g.mutate(ch)
	print "crossover all"
	g.crossover_all()
	g.selectionNat(nb_surv)
	#print g.pop
