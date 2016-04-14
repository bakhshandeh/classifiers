import utils 
import sys


if len(sys.argv) != 2:
    print "Usage: python create_idf_cutted.py MIN_DF"


db=utils.get_db_con()
cur=db.cursor()
cur.execute("SELECT content FROM newsitem where category is not NULL;")
words_dic={}
for row in cur.fetchall():
    # Simply counts the number of each word in the corpus
    # dic_word = {word1: count1, word2: count2, ...}
    for i in utils.tokenize(row[0]):
	if words_dic.has_key(i):
	    words_dic[i]+=1
	else:
	    words_dic[i]=1

# Reads the min DF from command line 
# For example if min_df = 2 we will remove the words that are just in 1 document
Count=int(sys.argv[1])
File=open('IDF.txt', 'w')
for i in words_dic:
    if words_dic[i]>Count:
	# Its important to encode the word
	File.write(i.encode("cp1252")+" "+str(words_dic[i])+"\n")
File.close()
