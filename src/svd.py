from __future__ import division
import json, math
import numpy as np

def getSVD(matrix):

	U, s, V = np.linalg.svd(matrix, full_matrices=False)
	
	U = np.matrix(U)
	s = np.matrix(np.diag(s))
	V = np.matrix(V)

	f = ((s.getI()).dot(U.getT()))

	return f, V

def loadMatrix(filename):

	loc = "../data/"+filename
	mat = np.genfromtxt(loc, delimiter=',')
	
	return mat

def writeData(filename, matrix):

	a = np.asarray(matrix)
	np.savetxt(filename, a, delimiter = ",")

def normalizeMat(matrix):

	num_col = len(matrix.tolist()[0])
	for i in range(num_col):
		_normalize_column(matrix, i)

	return matrix

def _normalize_column(A, col):
    
    A[:,col] = (A[:,col])/ np.linalg.norm(A[:,col])

def main():

	mat1 = loadMatrix("ConMatrix.csv")
	mat2 = loadMatrix("RepMatrix.csv")

	f1, V1 = getSVD(mat1)
	f2, V2 = getSVD(mat2)

	normalized_V1 = normalizeMat(V1)
	normalized_V2 = normalizeMat(V2)

	writeData("../data/func/con.csv", f1)
	writeData("../data/func/rep.csv", f2)

	writeData("../data/svd/reduced_con.csv", normalized_V1)
	writeData("../data/svd/reduced_rep.csv", normalized_V2)

if __name__ == '__main__':

	main()