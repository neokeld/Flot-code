#!/usr/bin/python
#
# genetic.py - A utility class to facilitate experimentation
# with genetic algorithm concepts.
#
# Version 1.0
# Project page: http://hobbiton.thisside.net/genetic/
# This software is provided under the BSD license:

"""
Copyright (c) 2003-2005, Rupert Scammell <rupe@sbcglobal.net>. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
    * notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above
    * copyright notice, this list of conditions and the following
    * disclaimer in the documentation and/or other materials provided
    * with the distribution.  Neither the name of Rupert Scammell
    * nor the names of its contributors may be used to endorse or
    * promote products derived from this software without specific
    * prior written permission.

	    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
	    CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
	    WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
	    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
	    PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
	    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
	    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
	    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
	    GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
	    BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
	    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
	    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
	    OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
	    POSSIBILITY OF SUCH DAMAGE.
"""
import sys, os, math, random

class Genetic:

	# Initialize values for genetic algorithm
	def __init__(self):
		# Operator list
		self.operator_list = []
		# Chromosome map
		self.chromosome_map = {}
		# Generation counter
		self.generation = 0
		# Chance of crossover (%/100)
		self.crossover_rate = 0.7
		# Chance of mutation (%/100)
		self.mutation_rate = 0.01
		# Desired value
		self.desired_value = 0
		# Number of operators (genes) in the chromosome
		self.operator_count = 0
		# Bits per gene
		self.bitcount = 0
		# Max value of bitstring 
		self.bitval = 1
		# Fitness value
		self.fitness_value = 0
		# List structure of chromosome data
		self.chromosome = []


	# Generate a random chromosome string
	def create_chromosome(self):
		random.seed()
		self.operator_count = len(self.operator_list)
		while (self.bitval < 60):
			self.bitcount = self.bitcount + 1
			self.bitval = self.bitval + (self.bitval * 2)
		for i in range(self.bitval):
			self.chromosome.append(str(random.randint(0,1)))
	
	# Build gene / operator mappings.
	def build_gene_map(self):
		for i in range(self.operator_count):
			current_bstring = str(self.int_to_bin(i))
			# Pad returned binary string to appropriate length.
			while (len(current_bstring) < self.bitcount+1):
				current_bstring = '0' + current_bstring

			self.chromosome_map[current_bstring] = {}
			self.chromosome_map[current_bstring]['op'] = str(self.operator_list[i])
			try:
				int(self.operator_list[i])
				self.chromosome_map[current_bstring]['type']='int'
			except ValueError:
				self.chromosome_map[current_bstring]['type'] = 'operator'
			
		
	# Do probablistic crossover operation.
	def crossover(self):
		self.crossover_point = random.randint(0,len(self.chromosome))
		if (random.random() <= self.crossover_rate):
			print '[crossover on %i]' % (self.crossover_point)
			self.chromosome = self.chromosome[self.crossover_point:] + \
			self.chromosome[:self.crossover_point]
	
	# Do probablistic mutation operation.
	def mutate(self):
		for i in range(len(self.chromosome)):
			if (random.random() <= self.mutation_rate):
				print '[mutation on %i]' % (i)
				if (self.chromosome[i] == '0'):
					self.chromosome[i] = '1'
				else:
					self.chromosome[i] = '0'
	
	# Compute result fitness using a simple rule.
	def fitness(self):
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