#!/usr/bin/python
#
# dna.py - A program to demonstrate applications of genetic algorithms.
# To use this program, provide a integer as the first argument, that you'd
# like to find an arithetic equivalent for (e.g. 4 -> 2+2, 2*2, 5-1, and so on)
# Large numbers may take a very long time to compute.
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


import sys, math, genetic

print 'Initializing genetic algorithm class...'
dna = genetic.Genetic()

# Define a list of allowable operators.
dna.operator_list = [0,1,2,3,4,5,6,7,8,9,"+","-","*","/"]
print 'Operator list: %s' % (str(dna.operator_list))

try:
    dna.desired_value = float(sys.argv[1])
except:
    print "============================"
    print "Donnez un entier en argument"
    print "============================"
    sys.exit(-1)

dna.create_chromosome()
print 'Initial chromosome is: %s' % (str(dna.chromosome))

print 'Building gene map from operator list...'
dna.build_gene_map()
print dna.chromosome_map

print 'Running genetic algorithm...'
current_fitness = 0

# Run until a solution is found.
while (dna.fitness_value != None):
	print 'Generation %i' % (dna.generation)
	dna.calculate_generation()
	print 'chromosome translation: %s' % (dna.eval_string)
	print 'result: %s' % (str(dna.current_result))
	
	if (dna.current_result != None):
		dna.fitness()
		print 'fitness value: %s' % (str(dna.fitness_value))
	print '---'
