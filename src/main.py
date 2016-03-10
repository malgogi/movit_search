from __future__ import division
import json, math
import numpy as np

def loadTermFile(rep_filename, con_filename):

	with open(rep_filename) as f:
		rep_terms = f.readline()

	with open(con_filename) as f:
		con_terms = f.readline()

	return eval(rep_terms), eval(con_terms)

def loadDocFile(doc_filename):
	
	with open(doc_filename) as f:
		docs = f.readline()

	return eval(docs)

def loadMatrix(filename):

	loc = "../data/"+filename
	mat = np.genfromtxt(loc, delimiter=',')
	
	return mat

def getQueryVec(query, rep_terms, con_terms):

	q = list(query.split())

	rep_query_vec = []
	con_query_vec = []

	for word in rep_terms:
		if word in q:
			rep_query_vec.append(q.count(word))
		else:
			rep_query_vec.append(0)

	for word in con_terms:
		if word in q:
			con_query_vec.append(q.count(word))
		else:
			con_query_vec.append(0)

	return np.matrix(rep_query_vec), np.matrix(con_query_vec)

def getReducedRepVec(repVec, func_rep):

	rV = np.matrix(repVec).getT()

	mag = np.linalg.norm(rV)
	if mag != 0 :
		rV = rV / mag

	return func_rep.dot(rV)

def getReducedConVec(conVec, func_con):

	cV = np.matrix(conVec).getT()

	mag = np.linalg.norm(cV)
	if mag != 0 :
		cV = cV / mag

	return func_con.dot(cV)

def calCossim(vec, matrix):

	score = (vec.getT()).dot(matrix)

	return score

def getResult(score):

	doc_num = len(score)
	res = []
	for i in range(doc_num):
		if score[i] > 2:
			res.append((i,0))
		else:
			res.append((i, score[i]))

	return sorted(res, key=lambda x:x[1], reverse=True)

def getFormatted(result, movies, docs, rank):

	res_list = []

	for i in range(rank):
		json_res = {}
		index, score = result[i]
		json_res["name"] = movies[index]["name"]
		json_res["rank"] = (i+1)
		json_res["imgs"] = movies[index]["imgs"]
		json_res["url"] = movies[index]["url"]
		json_res["actors"] = movies[index]["actors"]
		json_res["genre"] = movies[index]["genre"]
		json_res["date"] = movies[index]["date"]

		word_list = getTopWord(index, movies, 30)
		json_res["topWord"] = word_list

		res_list.append([json_res])

	return res_list

def getTopWord(index, movies, num):

	word_dict = {}

	movie = movies[index]

	rep_word = []

	for word in movie["reply_content"]["unigram"].keys():
		rep_word.append((word, movie["reply_content"]["unigram"][word]))

	rep_word = sorted(rep_word, key=lambda x:x[1], reverse=True)

	con_word = []

	for word in movie["movie_content"]["unigram"].keys():
		con_word.append((word, movie["movie_content"]["unigram"][word]))

	con_word = sorted(con_word, key=lambda x:x[1], reverse=True)
	
	for x in range(min(num, len(rep_word))):
		word, count = rep_word[x]
		if word in word_dict.keys():
			word_dict[word] += count
		else:
			word_dict[word] = count

	for x in range(min(num, len(con_word))):
		word, count = con_word[x]
		if word in word_dict.keys():
			word_dict[word] += count
		else:
			word_dict[word] = count

	return word_dict


def loadData(movie_file, collection_file):

	movies = json.loads(open(movie_file).read())
	collection = json.loads(open(collection_file).read())

	return movies, collection


def main():

	movies, collection = loadData("../data/formatted_docs.json", "../data/collection.json")

	rep_terms, con_terms = loadTermFile("../data/rep.txt", "../data/con.txt")
	
	docs = loadDocFile("../data/docs.txt")

	reduced_con = loadMatrix("../data/svd/reduced_con.csv")
	reduced_rep = loadMatrix("../data/svd/reduced_rep.csv")

	func_con = loadMatrix("../data/func/con.csv")
	func_rep = loadMatrix("../data/func/rep.csv")

	print("Loading done")

	weight = 0.5

	while True:
		#query = "googl internship silicon"
		query = raw_input("query?")

		repVec, conVec = getQueryVec(query, rep_terms, con_terms)

		reduced_repVec = getReducedRepVec(repVec, func_rep)
		reduced_conVec = getReducedConVec(conVec, func_con)

		score_rep = calCossim(reduced_repVec, reduced_rep)
		score_con = calCossim(reduced_conVec, reduced_con)

		total_score = score_con + score_rep
		total_score = total_score.tolist()[0]
		
		result = getResult(total_score)
		formatted_result = getFormatted(result, movies, docs, 30)

		print(json.dumps(formatted_result, indent=4, sort_keys=False))

if __name__ == '__main__':

	main()