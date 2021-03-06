import utils,sys
from sklearn.naive_bayes import GaussianNB

db=utils.get_db_con()
cur=db.cursor()
cur.execute("SELECT content, category FROM newsitem where category is not NULL;")
TFIDF_list=[]
label=[]
for row in cur.fetchall():
    TFIDF_list.append(utils.TF_naivebayse(utils.tokenize(row[0])))
    if row[1]==1 or row[1]==2 :
	label.append(1)
    else:
	label.append(0)

TFIDF_naive_bayse=[]
for i in TFIDF_list:
    TFIDF_naive_bayse.append(utils.TFIDF_to_list(i))

train_len=int(sys.argv[1])
indexZero=[i for i in range(len(label)) if label[i]==0][:train_len]
indexOne=[i for i in range(len(label)) if label[i]==1][:train_len]

train=[]
train_label=[]
for  i in indexZero+indexOne:
    train.append(TFIDF_naive_bayse[i])
    train_label.append(label[i])

test= [TFIDF_naive_bayse[i] for i in range(len(TFIDF_naive_bayse)) if i not in indexZero+indexOne]
test_label = [label[i] for i in range(len(label)) if i not in indexZero+indexOne]



nb = GaussianNB()
nb.fit(train, train_label)
counter1=0
TP=0
TN=0
FP=0
FN=0
for i in test:
    estimate_label=nb.predict([i])[0]
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
	estimate=nb.predict(utils.TFIDF_to_list(utils.TFIDF(utils.tokenize(row[0]))))
	cur.execute("update newsitem set "+column+"=" +str(estimate[0])+" where ID="+str(row[1])+";" )
	db.commit()
