import os
# Clearing the Screen
os.system('clear')
import time
import numpy as np
import math
import random
import sys
cI = complex(0,1)

import grassmanntn as gtn
from grassmanntn.grassmanntn import dense
from grassmanntn.grassmanntn import sparse
from grassmanntn import param

def main():

	#test_svd()
	#test_trg()
	test_einsum()

	exit()

#----------------------------------------------------------------------------------#

def test_svd():

	# Starting with a random complex 4-legged tensor

	n=4
	A = gtn.random( (n,n,n,n) , (1,1,-1,-1), tensor_format=dense, dtype=complex)
	U, S, V = A.svd('ij,kl')

	# Obtain a square-root singular value tensor
	# The square root must be done in the matrix format only!

	S = S.switch_format()
	sqrtS = S.copy()
	sqrtS.data = np.sqrt(S.data)

	# Contraction

	X = gtn.einsum('ijx,xk->ijk',U,sqrtS)
	Y = gtn.einsum('kx,xij->kij',sqrtS,V)
	A2 = gtn.einsum('ijx,xkl->ijkl',X,Y)

	A.info()
	A2.info()

	print((A-A2).norm)
	print()

	return 1

def test_trg():

	n=4
	A = gtn.random( (n,n,n,n) , (1,1,-1,-1), tensor_format=dense, dtype=complex)

	gtn.trg(A,n**2)

	return 1

def test_einsum():

	# Starting with a random complex 4-legged tensor

	n=8
	A = gtn.random( (n,n,n,n) , (1,1,-1,-1), tensor_format=dense, dtype=complex)
	B = gtn.random( (n,n,n,n) , (1,1,-1,-1), tensor_format=dense, dtype=complex)

	C1 = gtn.einsum('i1 i2 k1 k2, k1 k2 i3 i4-> i1 i2 i3 i4',A,B)
	C2 = gtn.einsum('ijab,abkl->ijkl',A,B)

	print( (C1-C2).norm )

	n = 4
	A = gtn.random( (n,3,3) , (1,0,0), tensor_format=sparse, dtype=float)
	B = gtn.random( (n,3,3) , (-1,0,0), tensor_format=sparse, dtype=float)
	C = gtn.einsum( 'amn,amn->mn', A,B)

	A.display()
	B.display()
	C.display()

	return 1

main()