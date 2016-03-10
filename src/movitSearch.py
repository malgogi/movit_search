from __future__ import division
import json, math
import numpy as np

class MovitSearch( object ):

	DATA_PATH_PREFIX = "../data"
	weight = 0.5

	def loadTermFile(self, rep_filename, con_filename):

		with open(rep_filename) as f:
			rep_terms = f.readline()

		with open(con_filename) as f:
			con_terms = f.readline()

		return eval(rep_terms), eval(con_terms)

	def loadDocFile(self, doc_filename):
		
		with open(doc_filename) as f:
			docs = f.readline()

		return eval(docs)

	def loadMatrix(self, filename):
		mat = np.genfromtxt( filename, delimiter=',')
		
		return mat

	def getQueryVec(self, query, rep_terms, con_terms):

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

	def getReducedRepVec(self, repVec, func_rep):

		rV = np.matrix(repVec).getT()

		mag = np.linalg.norm(rV)
		if mag != 0 :
			rV = rV / mag

		return func_rep.dot(rV)

	def getReducedConVec(self, conVec, func_con):

		cV = np.matrix(conVec).getT()

		mag = np.linalg.norm(cV)
		if mag != 0 :
			cV = cV / mag

		return func_con.dot(cV)

	def calCossim(self, vec, matrix):

		score = (vec.getT()).dot(matrix)

		return score

	def getResult(self, score):

		doc_num = len(score)
		res = []
		for i in range(doc_num):
			if score[i] > 2:
				res.append((i,0))
			else:
				res.append((i, score[i]))

		return sorted(res, key=lambda x:x[1], reverse=True)

	def getFormatted(self, result, movies, docs, rank):

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
			json_res["content"] = movies[index]["content"].replace("<s>", "").replace("</s>", "")

			word_list = self.getTopWord(index, movies, 30)
			json_res["topWord"] = word_list

			res_list.append( json_res )

		return res_list

	def getTopWord(self, index, movies, num):

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


	def loadData(self, movie_file, collection_file):

		movies = json.loads(open(movie_file).read())
		collection = json.loads(open(collection_file).read())

		return movies, collection

	def getRanking( self, query ):
		repVec, conVec = self.getQueryVec(query, self.rep_terms, self.con_terms)

		reduced_repVec = self.getReducedRepVec(repVec, self.func_rep)
		reduced_conVec = self.getReducedConVec(conVec, self.func_con)

		score_rep = self.calCossim(reduced_repVec, self.reduced_rep)
		score_con = self.calCossim(reduced_conVec, self.reduced_con)

		total_score = score_con + score_rep
		total_score = total_score.tolist()[0]
		
		result = self.getResult(total_score)
		formatted_result = self.getFormatted(result, self.movies, self.docs, 30)

		#print(json.dumps(formatted_result, indent=4, sort_keys=False))
		return json.dumps(formatted_result)

	def __init__( self ):
		print( 'init module' )
		self.movies, self.collection = self.loadData( self.DATA_PATH_PREFIX + "/formatted_docs.json", self.DATA_PATH_PREFIX + "/collection.json")

		self.rep_terms, self.con_terms = self.loadTermFile( self.DATA_PATH_PREFIX + "/rep.txt", self.DATA_PATH_PREFIX + "/con.txt")
		
		self.docs = self.loadDocFile( self.DATA_PATH_PREFIX + "/docs.txt")

		self.reduced_con = self.loadMatrix( self.DATA_PATH_PREFIX + "/svd/reduced_con.csv")
		self.reduced_rep = self.loadMatrix( self.DATA_PATH_PREFIX + "/svd/reduced_rep.csv")

		self.func_con = self.loadMatrix( self.DATA_PATH_PREFIX + "/func/con.csv")
		self.func_rep = self.loadMatrix( self.DATA_PATH_PREFIX + "/func/rep.csv")
		print 'end module'