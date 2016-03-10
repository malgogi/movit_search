from __future__ import division
import json, math
import numpy as np

def setConMatrix(con_terms, docs, movies):
	''' Set Contents Matrix '''
	
	m = []
	movie_num = len(docs)

	for x in range(movie_num):
		col = []
		for term in con_terms:
			if term in movies[x]["movie_content"]["unigram"].keys():
				col.append(movies[x]["movie_content"]["unigram"][term])
			else:
				col.append(0)
		m.append(col)

	mat = np.matrix(m)
	mat = mat.getT()

	return mat

def setRepMatrix(rep_terms, docs, movies):
	''' Set Reply Matrix  '''

	m = []
	movie_num = len(docs)

	for x in range(movie_num):
		col = []
		for term in rep_terms:
			if term in movies[x]["reply_content"]["unigram"].keys():
				col.append(movies[x]["reply_content"]["unigram"][term])
			else:
				col.append(0)
		m.append(col)

	mat = np.matrix(m)
	mat = mat.getT()

	return mat

def setTerm(name, collection):
	''' Set Term list storing order of terms '''

	s = name + "_content"

	terms = []

	for term in collection[s]["unigram"].keys():
		terms.append(term)

	return terms

def setDocument(movies):
	''' Set Document list, storing order of documents(movies) '''

	docs = []

	for movie in movies:
		docs.append(movie["name"])

	return docs

def loadData(movie_file, collection_file):

	movies = json.loads(open(movie_file).read())
	collection = json.loads(open(collection_file).read())

	return movies, collection

def writeCSV(filename, matrix):

	a = np.asarray(matrix)
	np.savetxt(filename, a, delimiter = ",")

def writeFile(filename, array):

	with open(filename, "w") as f:
		f.write(array)

def main():

	movies, collection = loadData("../data/formatted_docs.json", "../data/collection.json")
	
	col_conlen = collection["movie_content"]["unigram_length"]
	col_replen = collection["reply_content"]["unigram_length"]

	rep_terms = setTerm("reply", collection)
	writeFile("../data/rep.txt", json.dumps(rep_terms))

	con_terms = setTerm("movie", collection)
	writeFile("../data/con.txt", json.dumps(con_terms))

	docs = setDocument(movies)
	writeFile("../data/docs.txt", json.dumps(docs))

	m1 = setConMatrix(con_terms, docs, movies)
	writeCSV("../data/ConMatrix.csv", m1)

	m2 = setRepMatrix(rep_terms, docs, movies)
	writeCSV("../data/RepMatrix.csv", m2)

	

if __name__ == '__main__':

	main()

