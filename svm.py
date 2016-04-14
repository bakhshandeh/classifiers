import utils,sys
from sklearn import svm



db=utils.get_db_con()
cur=db.cursor()
cur.execute("SELECT content, category FROM newsitem where category is not NULL;")
TFIDF_list=[]
label=[]

for row in cur.fetchall():
    TFIDF_list.append(utils.TFIDF(utils.tokenize(row[0])))
    # category 1,2: label=1
    if row[1]==1 or row[1]==2 :
	label.append(1)
    else:
	# category 3: labe=0
	label.append(0)

TFIDF_svm=[]
for i in TFIDF_list:
    TFIDF_svm.append(utils.TFIDF_to_list(i))
# TFIDF_svm is the input matrix of SVM

# Reads the train_len from command line
train_len=int(sys.argv[1])

# Index of train samples from class 0
indexZero=[i for i in range(len(label)) if label[i]==0][:train_len]
# Index of train samples from class 1
indexOne=[i for i in range(len(label)) if label[i]==1][:train_len]
# We have K number of positive samples and also K number of negative samples

train=[]
train_label=[]
for  i in indexZero+indexOne:
    train.append(TFIDF_svm[i])
    train_label.append(label[i])
# Train: train matrix
# train_label: lables of train data

# The other samples are test samples.
test = [TFIDF_svm[i] for i in range(len(TFIDF_svm)) if i not in indexZero+indexOne]
test_label = [label[i] for i in range(len(label)) if i not in indexZero+indexOne]


clf = svm.SVC()
# Train the model
clf.fit(train, train_label)

counter1=0

#True positives
TP=0
#True negatives
TN=0
#False positives
FP=0
#False negatives
FN=0


for i in test:
    estimate_label=clf.predict([i])[0]
    if estimate_label==1 and label[counter1]==1:
	TP+=1
    elif estimate_label==1 and label[counter1]==0:
	FN+=1
    elif estimate_label==0 and label[counter1]==0:
	TN+=1
    else:
	FP+=1
    counter1+=1
    print counter1

print 'TP=>',TP , 'FN=>',FN, 'FP=>',FP,'TN=>', TN
print 'Precision: ', float(TP)/(TP+FP)
print 'Recall: ', float(TP)/(TP+FN)
print 'Accuracy: ', float(TP+TN)/(TP+FN+FP+TN)
print float(TP+TN)/(TP+FN+FP+TN), float(TP)/(TP+FP), float(TP)/(TP+FN), TP, FN, FP, TN



if "--update-db" in sys.argv:
    cur.execute("SELECT content, ID  FROM newsitem;")
    column=sys.argv[-1]
    for row in cur:
	estimate=clf.predict(utils.TFIDF_to_list(utils.TFIDF(utils.tokenize(row[0]))))
	cur.execute("update newsitem set "+column+"=" +str(estimate[0])+" where ID="+str(row[1])+";" )
	db.commit()
