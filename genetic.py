#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# genetic.py - A utility class to facilitate experimentation
# with genetic algorithm concepts.
#
# Version 1.0
# Project page: http://hobbiton.thisside.net/genetic/
# This software is provided under the BSD license:

import sys, os, math, random, MSTKruskal, UnionFind, Chargement

class Genetic:

	# Initialize values for genetic algorithm
	# Param : max_nb_gen : nombre maximum de generation
	def __init__(self, max_nb_gen, crossover_rate, mutation_rate, K, nb_node):
	
	
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
		# Taille de la population
		self.taille_population = 0
		# Longueur de cycle Max :
		self.K = K
		# nombre de noeud
		self.nb_node = nb_node 
		# liste des chromosomes, c'est notre population
		self.pop = []
		# Profondeur de parcours max
		self.profondeur = 4


	# Generate a random chromosome string
	def create_first_population(self):
		print "create"
		print
		# le premier chromosome de base
		M=Chargement.EuclideanDistMatrix("./dev/data/n40-2")
		F=MSTKruskal.MinimumSpanningTree(M)	
		self.graph = MSTKruskal.convertToAdjacent(F, M)
			

	# Build gene / operator mappings.
	def build_gene_map(self):
		print "build gene map"

		
	# Do probablistic crossover operation.
	def crossover(self, i, j):
		print "crossover"
		random.seed()
		chrom1 = self.pop[i]
		chrom2 = self.pop[j]
		new_chrom = [[0,0]*self.K]
		# pour chaque noeud
		for k in range(nb_node):
		    # il faut choisir un cycle parmi les deux chromosomes 
		    r = random.randint(0,1)
		    if r == 0 :
			# on prend un bout de gene, ie on prend un cycle parmi tous les cyles du noeud k pour le chrom1
			new_chrom[k] = chrom1[k][random.randint(0,len(chrom1[k]))]
		    else :
			new_chrom[k] = chrom2[k][random.randint(0,len(chrom2[k]))]

		print new_chrom
		self.pop.append(new_chrom)

		# maintenant on a pour chaque noeud un cycle
		# il faut toutefois retravaillé pour que chaque noeud il y ait l'ensemble des cycles
	
		#TODO

	# fait l'ensemble des crossovers pour une génération
	def crossover_all(self):
	    random.seed()

	    for i in range(self.taille_population):
		r = rand(0,1)
		if r <= crossover_rate :
		    # ce chromosome va subir un crossover
		    ri = randint(0, self.taille_population)
		    if ri != i :
			crossover(i,ri)
	    print self.pop


	# Fait une mutation i(probabiliste, peut ne pas faire de mutation dans certains cas)
	def mutate(self, chromo, cycle):
		print "mutate"
		# on prend 1 noeud au hasard
		random.seed()
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

		print "f :"
		print f
		if f != []:
		    f.pop(0)
		    # on ajoute le chemin f trouvé dans l'ancien cycle
		    cycle[n1+1:n1+1] = f
		# on ajoute le cycle dans le chromosome
		chromo.append(cycle)


	# Compute result fitness using a simple rule.
	def fitness(self):
		print "fitness"
		try:
			self.fitness_value = 1 / (self.desired_value - self.current_result)
		# A correct solution will return a divide by zero error.
		except:
			self.fitness_value = None 
	
	# Integer to binary string conversion.
	def int_to_bin(self, i):
		s = ""
		while i:
			s= (i & 1 and '1' or '0') + s
			i >>= 1
		return s or '0'
		
	# Calculate value for the current chromosome generation.
	def calculate_generation(self):
		print "calculate generation"
		# Result generated by the current generation of chromosome.
		self.current_result = 0
		# String generated from chromosome operators, used for evaluation.
		self.eval_string = ""
		# Last type of gene encountered in the chromosome.  Needed for type alternation.
		last_type = ""
		
		# Mutate and crossover operations on chromosome
		self.mutate()
		self.crossover()
		
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
					(chromosome_type == "operator"):
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

if __name__ == '__main__':
    max_nb_gen = 8
    crossover_rate = 0.7
    mutation_rate = 0.5
    K = 4
    nb_node = 7
    g = Genetic(max_nb_gen, crossover_rate, mutation_rate, K, nb_node )
    g.create_first_population()
    g.crossover_all()
    chromo = [[]]
    cycle = [0, 2, 3, 6, 5, 1]
    g.mutate(chromo, cycle)
    print "chromo :"
    print chromo