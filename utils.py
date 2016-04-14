# -*- coding: cp1252 -*-
import MySQLdb
import math
import re, sys, nltk

IDF_dic={}
stopwords=[]

"""
    We will use this function to connect to DB.
    @return	a MySQL object
"""
def get_db_con():
    # To change the MySQL settings you just need to change this line
    con = MySQLdb.connect(host="localhost",  user="db_user", passwd="db_pass",  db="textp") 
    return con

"""
    This function gets a list of words and returns a 
    list of preprocessed and stemmed words
    
    @param	word_list list
    @return	list of preprocessed and stemmed words
"""
def preprocess(word_list):
    preprocess_list=[]
    excludechars = re.compile(r'[()&#%|@><_*+$./[?!,\'":;0-9\\\]]')
    for word in word_list:
	word = excludechars.sub("", word)
	word = word.replace("â€“", "-")
        word = word.replace(" œ", "`")
        word = word.replace("`™", "`")
        word = word.replace("â©", "`")
        word = word.replace("â€˜ ", "`")
        word = word.replace("˜ ", "`")
        word = word.replace("â€", "`")
        word = word.strip( '-' )
        word = word.strip( '=' )
        word = word.strip( ',' )
        word = word.strip( '`' )
        word = word.replace("â€™", "'")
        word = word.replace("ã«", "e")
        word = word.replace("ã©", "e")
        word = word.replace("ã¶", "o")
        word = word.replace("ã¯", "i")
        word = word.replace("â€œ", "")
        word = word.replace("â€¦", "...")
        word = word.replace("ã¼", "u")
        word = word.replace("ã", "")
        preprocess_list.append(word)
    # Use snowball stemmer
    stemmer = nltk.stem.snowball.DutchStemmer()
    
    # Its very important to convert the words to unicode. Otherwise python throws UnicodeError
    stemmed_words = [stemmer.stem(unicode(i, "cp1252")) for i in preprocess_list]
    
    # The return is a list of tokenized and stemmed words.
    return stemmed_words

"""
    This function gets a string(raw text) and tokenize it
    and returns a list of preprocesed and stemmed words.
    
    @param		text string
    @return		list of stemmed words
"""
def tokenize(text):
    # List of delimiters
    list_delimiter=['.',',', '#', '-','@', '\r', '\n']
    
    # We first replace all of delimiters with space and then split the string
    for i in list_delimiter:
	text=text.replace(i, ' ')
    word_list=text.split(' ')
    word_list=preprocess(word_list)
    # len(j) > 0: filters empty strings
    return  [j for j in  word_list if len(j)>0]
    

"""
    Reads the stopwords and creates a global list
"""
def load_stopwords():
    global stopwords
    File=open('stopwords.txt','r')
    for line in File.readlines():
	stopwords.append(line.replace('\n','').decode('cp1252'))

"""
    Returns the term frequency of the word.
    Returns 0 if the word is in the stopwords
    
    @param		words_list	list
    @param		word		string
    @return		int term frequency of word
"""
def TF(words_list, word):
    global stopwords
    if len(stopwords)==0:
	load_stopwords()
    if word in words_list and word not in stopwords:
	return words_list.count(word)
    else:
	return 0

"""
    This function loads the IDF file into a global dictionary.
    So we can use it in all of the functions.
    
    IDF_dic: {word1: DF1, word2: DF2, ...}
"""
def load_IDF():
    global IDF_dic
    File=open('IDF.txt','r')
    for line in File.readlines():
	cells=line.decode('cp1252').split(' ')
	IDF_dic[cells[0]]=cells[1]

"""
    Calculates the TFIDF vector.
    
    @param	words_list	list of the words
    @return	TFIDF dic	{word1: tfidf1, word2: tfidf2, ...}
"""
def TFIDF(words_list):
    global IDF_dic
    TFIDF_dic={}
    if len(IDF_dic)==0:
	load_IDF()
    for i in words_list:
	#print type(i)
	#print type(IDF_dic[i])
	if IDF_dic.has_key(i):
	    # This is the magic line
	    # TFIDF(w) = TF(w)*log(N/IDF(w))
	    # N is total number of documents. So If you want to change the dataset
	    # you should change the 500
	    TFIDF_dic[i]=TF(words_list, i)*math.log(500.00/int(IDF_dic[i]))
    return TFIDF_dic

"""
    Calculates the distance between 2 TFIDF array
    
    @param	dic1	TFIDF dic of doc1
    @param	dic2	TFIDF dic of doc2
    
    @return	float	Euclidean distance
"""
def TFIDF_distance(dic1, dic2):
    Sum=0
    # list(set(words1+words2)): a uniq list of all the words in doc1 and doc2
    for word in list(set(dic1.keys()+dic2.keys())):
	coun1=dic1[word] if dic1.has_key(word) else 0
	coun2=dic2[word] if dic2.has_key(word) else 0
	Sum+=(coun1-coun2)**2
    return Sum

"""
    For SVM and naive bayse algorithms we need to convert
    the TFIDF dic to a list in this format: [TFIDF(word_1), TFIDF(word_2), ... , TFIDF(word_N)]
    Note that N is total number of words and length of the list is same as the length of IDF array
    
    @param	TFIDF_dic	dic {word1: tfidf1, word2:tfidf2, ...}
    @return	list		[TFIDF(word1), TFIDF(word2), ...]
"""
def TFIDF_to_list(TFIDF_dic):
    global IDF_dic
    TFIDF_list=[]
    if len(IDF_dic)==0:
	load_IDF()
    for i in IDF_dic:
	if TFIDF_dic.has_key(i):
	    TFIDF_list.append(TFIDF_dic[i])
	else:
	    TFIDF_list.append(0)
    return TFIDF_list

"""
    This function creates the input list for Naive Bayse/bag of words
    
    @param	words_list	list of words of a document
    @return	list [TF(w1), TF(w2), ...]: All of the words of the dataset are in this list
"""
def TF_naivebayse(words_list):
    TF_dic={}
    for i in words_list:
	TF_dic[i]=TF(words_list, i)
    return TF_dic
