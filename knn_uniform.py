import utils,sys
k=5


db=utils.get_db_con()
cur=db.cursor()
cur.execute("SELECT content, category FROM newsitem where category is not NULL;")
TFIDF_list=[]
label=[]
for row in cur.fetchall():
    TFIDF_list.append(utils.TFIDF(utils.tokenize(row[0])))
    if row[1]==1 or row[1]==2 :
	label.append(1)
    else:
	label.append(0)

counter1=0
TP=0
TN=0
FP=0
FN=0
while counter1 < len(TFIDF_list):
    distance_list=[]
    counter2=0
    while counter2< len(TFIDF_list):
	if counter1 !=counter2:
	    distance_list.append(utils.TFIDF_distance(TFIDF_list[counter1], TFIDF_list[counter2]))
	counter2+=1
    nearest_list=sorted(range(len(distance_list)), key=lambda i:distance_list[i])[:k]
    repeat_dic={}
    for i in  nearest_list:
	if repeat_dic.has_key(label[i]):
	    repeat_dic[label[i]]+=1
	else:
	    repeat_dic[label[i]]=1
    estimate_label=max(repeat_dic, key=repeat_dic.get)
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
	data=utils.TFIDF(utils.tokenize(row[0]))
	distance_list=[]
	for i in  range(len(TFIDF_list)):
	    distance_list.append(utils.TFIDF_distance(data, TFIDF_list[i]))
	nearest_list=sorted(range(len(distance_list)), key=lambda i:distance_list[i])[:k]
	repeat_dic={}
        for i in  nearest_list:
    	    if distance_list[i] !=0:
		if repeat_dic.has_key(label[i]):
		    repeat_dic[label[i]]+=1
		else:
		    repeat_dic[label[i]]=1
	estimate=max(repeat_dic, key=repeat_dic.get)
	cur.execute("update newsitem set "+column+"=" +str(estimate)+" where ID="+str(row[1])+";" )
	db.commit()
