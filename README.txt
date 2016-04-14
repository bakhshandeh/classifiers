
Requirements:
1- MySQLdb
2- sklearn
3- nltk

How to run:

1- Create IDF.txt file:
python create_idf_cutted.py MIN_DF
Example: create_idf_cutted.py 1
This command will create IDF.txt files and removes the words that is just in 1 document(IDF=1).

2- Run the algs:

KNN:
python knn_uniform.py
python knn_distance_weights.py

SVM:
python svm.py K
Example: python svm.py 100
It will select 2*K train samples; K class #1 and K class #0.

Naive bayse/TFIDF:
python naive_bayes.py K

Naive Bayse/ Bag of words:
python TF_naive_bayes.py K

